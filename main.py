import os
import sys
from dotenv import load_dotenv
from src.content_engine import ContentEngine
from src.blogger_client import BloggerClient

# 환경 변수 로드
load_dotenv()

def main():
    # 1. 구성 확인
    # Standardize environment variable names
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    client_id = os.getenv("CLIENT_ID") or os.getenv("BLOGGER_CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET") or os.getenv("BLOGGER_CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN") or os.getenv("BLOGGER_REFRESH_TOKEN")
    blog_id = os.getenv("BLOG_ID") or os.getenv("BLOGGER_BLOG_ID")

    if not all([gemini_key, client_id, client_secret, refresh_token, blog_id]):
        print("환경 변수가 누락되었습니다. .env 파일이나 GitHub Secrets를 확인해주세요.")
        # 디버깅을 위해 어떤 키가 누락되었는지 출력 (보안을 위해 값은 출력하지 않음)
        missing = []
        if not gemini_key: missing.append("GEMINI_API_KEY/GOOGLE_API_KEY")
        if not client_id: missing.append("CLIENT_ID/BLOGGER_CLIENT_ID")
        if not client_secret: missing.append("CLIENT_SECRET/BLOGGER_CLIENT_SECRET")
        if not refresh_token: missing.append("REFRESH_TOKEN/BLOGGER_REFRESH_TOKEN")
        if not blog_id: missing.append("BLOG_ID/BLOGGER_BLOG_ID")
        print(f"누락된 키: {', '.join(missing)}")
        sys.exit(1)

    # 2. 시스템 초기화
    content_engine = ContentEngine(gemini_key)

    # 3. 주제 선택
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        print("현재 트렌딩 주제를 검색(추천) 중입니다...")
        topic = content_engine.recommend_topic()

    print(f"선정된 주제: {topic}")

    # 4. 콘텐츠 생성
    print("Gemini로 콘텐츠 생성 중...")
    raw_content = content_engine.generate_content(topic)
    
    if not raw_content:
        print("\n" + "="*50)
        print("CRITICAL ERROR: 콘텐츠 생성에 실패했습니다.")
        print("원인: API 할당량 초과(Quota Exceeded) 또는 일시적인 네트워크 오류일 수 있습니다.")
        print("도움말: 'gemini-3-flash-preview' 모델을 사용 중입니다. 쿼터 또는 API 키 활성화 상태를 확인해주세요.")
        print("해결책: 수동 실행 시 주제를 직접 전달하여 추천 API 호출을 줄이거나, 다음 날 다시 시도하세요.")
        print("="*50 + "\n")
        sys.exit(1)

    cleaned_content = content_engine.clean_html(raw_content)
    tags = content_engine.extract_tags(cleaned_content)
    
    # 5. 제목 추출 루틴
    import re
    # 우선 <h1> 태그를 찾고, 없으면 주제를 사용합니다.
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', cleaned_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        post_title = re.sub('<[^<]+?>', '', title_match.group(1)).strip()
    else:
        post_title = topic
    print(f"제목: {post_title}")
    print(f"태그: {tags}")

    # 6. Blogger에 업로드 (초안으로)
    print("Blogger에 업로드 중...")
    blogger = BloggerClient(client_id, client_secret, refresh_token, blog_id)
    result = blogger.create_post(
        title=post_title,
        content=cleaned_content,
        labels=tags,
        is_draft=True # 사람이 검토할 수 있도록 초안으로 시작
    )

    if result:
        print("워크플로우 완료.")
    else:
        print("업로드 단계에서 워크플로우 실패.")
        sys.exit(1)

if __name__ == "__main__":
    main()
