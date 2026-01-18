import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class BloggerClient:
    def __init__(self, client_id, client_secret, refresh_token, blog_id):
        self.blog_id = blog_id
        self.scopes = ['https://www.googleapis.com/auth/blogger']
        
        # Validation
        if not all([client_id, client_secret, refresh_token]):
            missing = []
            if not client_id: missing.append("CLIENT_ID")
            if not client_secret: missing.append("CLIENT_SECRET")
            if not refresh_token: missing.append("REFRESH_TOKEN")
            print(f"--- [AUTH ERROR] Missing credentials: {', '.join(missing)} ---")

        # 토큰에서 직접 자격 증명 객체 생성
        self.creds = Credentials(
            None, 
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=self.scopes
        )

    def get_service(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    print("--- [AUTH] Attempting to refresh access token... ---")
                    self.creds.refresh(Request())
                    print("--- [AUTH] Token refreshed successfully. ---")
                except Exception as e:
                    print(f"--- [AUTH ERROR] Token refresh failed: {e} ---")
                    print("\n" + "!" * 50)
                    print("CRITICAL: Blogger 인증에 실패했습니다 (invalid_grant).")
                    print("원인: 리프레시 토큰이 만료되었거나 취소되었습니다.")
                    print("해결 방법:")
                    print("  1. 로컬에서 'python get_token.py'를 실행하여 새 토큰을 얻으세요.")
                    print("  2. 새 토큰을 .env 파일이나 GitHub Secrets에 업데이트하세요.")
                    print("  3. (권장) Google Cloud Console에서 'OAuth 동의 화면' -> '앱 게시'를 수행하여 7일 제한을 해제하세요.")
                    print("!" * 50 + "\n")
                    raise
        
        return build('blogger', 'v3', credentials=self.creds)

    def create_post(self, title, content, labels=None, is_draft=True):
        service = self.get_service()
        
        body = {
            'kind': 'blogger#post',
            'blog': {'id': self.blog_id},
            'title': title,
            'content': content,
        }
        
        if labels:
            body['labels'] = labels

        print(f"--- [DEBUG] Blogger API 요청 데이터 구성 완료 ---")
        print(f"--- [DEBUG] Title: {body.get('title')} ---")
        print(f"--- [DEBUG] Content Length: {len(body.get('content', ''))} ---")

        try:
            posts = service.posts()
            # is_draft가 True이면 초안으로 저장됩니다 (기본 동작은 보통 명시적인 게시 작업이나 상태가 필요함)
            # insert 메서드에는 'isDraft' 매개변수가 있습니다.
            result = posts.insert(blogId=self.blog_id, body=body, isDraft=is_draft).execute()
            print(f"게시글 생성 성공: {result.get('url')}")
            return result
        except Exception as e:
            print(f"게시글 생성 중 오류 발생: {e}")
            return None
