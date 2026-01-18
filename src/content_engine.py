import os
import re
from datetime import datetime
from google import genai
from google.genai import types

class ContentEngine:
    def __init__(self, api_key):
        # google-genai SDK 사용
        self.client = genai.Client(api_key=api_key)
        # 사용자의 요청에 따라 gemini-2.5-flash-lite 모델 사용
        self.model_id = 'gemini-2.5-flash-lite'

    def recommend_topic(self):
        """
        Gemini를 사용하여 최근 시장 트렌드에 맞는 기업을 추천받습니다.
        """
        prompt = """
        당신은 금융 시장 트렌드 스카우터입니다.
        다음 조건에 맞는 **단 하나의 상장 기업**을 찾아 추천해주세요. (S&P 500 지수 포함 기업 위주)

        **조건**:
        1. 최근 주요 금융 뉴스나 Reddit에서 화제가 되고 있는 기업.
        2. 메이저 빅테크(NVDA, AAPL 등) 제외.
        
        **결과물**: 오직 **기업명(티커)** 만 출력하세요. (예: Ford Motor (F))
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            if not response.text:
                raise ValueError("Response text is empty")
            return response.text.strip()
        except Exception as e:
            print(f"\n--- 주제 추천 중 오류 발생 ---")
            print(f"Error: {e}")
            return "NVIDIA (NVDA)"

    def generate_content(self, topic):
        """
        [투자분석 블로그 통합 프롬프트 시스템 v3.0]을 온전히 적용하여 콘텐츠를 생성합니다.
        """
        full_prompt = f"""
        당신은 20년 경력의 가치 투자 분석가입니다. 이번 분석 주제는 **"{topic}"** 입니다. 
        아래의 **[1. 스타일 가이드]**를 최우선으로 준수하면서, **[2. 통합 프롬프트 시스템 v3.0]**의 모든 내용을 생략 없이 반영하여 최상의 결과를 도출하세요.

        ---

        ### 1. 스타일 가이드 (최우선 준수)
        - **문체**: 모든 문장은 기본적으로 **'~이다'** 체(평서문)를 사용한다.
        - **사견 및 통찰**: 종종 글의 흐름에 당신의 주관적인 사견을 자연스럽게 섞는다. 이는 불확실한 인사이트여도 괜찮다.
           - 개인적인 경험을 녹여낸 1인칭 관찰자 시점의 문체를 사용하라. 문장은 화려하지 않고 수수해야야 한다. 해당 문장은 어두운회색 색상으로 표시한다 태그로 감싸서 취소선 처리한다.
        - **영어 라벨 금지**: 본문의 소제목(Header)이나 섹션 구분 시 "Stage 1", "Phase 1"과 같이 영어로 단계를 명시하지 않는다. 오직 한국어 제목만 사용한다.
        - **페르소나 언급 금지**: 본문에서 "나는 신중한 역발상 투자자이다"와 같이 자신의 정체성을 구구절절 밝히지 않는다. 오직 분석의 깊이로 증명한다.
        - **투자의견 조절**: 의견을 너무 강요하거나 확정적으로 말하지 말고, **신중하고 보수적인 관점**에서 부드럽게 표현한다.
        - **영문 병기 금지**: 괄호 안에 불필요한 영문 번역 명칭을 넣지 않는다. 꼭 필요한 경우를 제외하고는 한국어만 사용한다.
        - **용어 사용 주의**: '악마의 변호인'이라는 단어를 본문에 직접 노출하지 않는다. 대신 리스크 분석, 반론, 혹은 '고려해야 할 위험 요소' 등으로 자연스럽게 표현한다.

        ---

        ### 2. 통합 프롬프트 시스템 v3.0

        ## Layer 1: Design System Foundation
        ### 1.1 디자인 철학
        ### 🎨 기본 기조
        > "신뢰를 통한 설득" - 복잡한 금융 정보를 단순하고 명확하게 전달
        ### 📐 디자인 3대 원칙
        1. **Minimal Complexity**: 복잡한 금융 정보를 단순하고 명확하게
        2. **Data-First but easy readable**: 가독성 좋고 긍정/부정이 한눈에 들어오게 함
        3. **Trust Through Consistency**: 일관성으로 전문성 구축

        ### 1.2 CSS 변수 체계
        ```css
        :root {{
          --color-primary: #1A1A2E;         /* 다크 네이비 */
          --color-secondary: #0F4C75;       /* 딥 블루 */
          --color-accent-positive: #16C79A; /* 상승 */
          --color-accent-negative: #FF6B6B; /* 하락 */
          --color-background: #FFFFFF;
          --color-text-primary: #2C3E50;
        }}
        ```

        ---

        ## Layer 2: HTML Structure Framework
        ### 2.1 구조 설계 철학
        ### 📋 구조 설계 4대 원칙
        1. **Platform Awareness**: 스킨 시스템 충돌 방지, 에디터 자동 변환 대응
        2. **EEAT**: 작성자 푸터 포함 (작성자:우디(Woody), AI를 활용한 실전 투자자 분석가)

        ### 2.2 5-Phase 템플릿 구조
        (Phase 1: Meta Header, Phase 2: Navigation, Phase 3: Main Content, Phase 4: Compliance Footer, Phase 5: Inline Styles)

        ---

        ## Layer 3: Content Generation Engine
        ### 3.1 역할 정의
        ### 👤 페르소나
        **'Prudent Contrarian'** - 20년 경력 가치투자 애널리스트
        ### 3.2 6단계 분석 프레임워크
        - Stage 1: 기업 본질 분석 (비즈니스 모델, 점유율 등)
        - Stage 2: 재무 건전성 분석 (ROE, 영업이익률, FCF, 부채비율 등)
        - Stage 3: 시나리오 분석 (Bull, Base, Bear)
        - Stage 4: 밸류에이션 종합 (DCF, P/E, P/B, 안전마진 10%)
        - Stage 5: 투자 의사결정 (STRONG BUY ~ STRONG SELL)
        - Stage 6: 메타인지 검증 (편향 점검)

        ---

        **형식 요구사항**:
        - 출력 형식: **완전한 HTML 문서 (Full HTML Document)** 형식으로 작성하라.
        - 필수 포함 태그: `<!DOCTYPE html>`, `<html lang="ko">`, `<head>`, `<title>`, `<style>`, `<body>`.
        - **CSS 처리**: 위에서 정의한 '1.2 CSS 변수 체계'와 모든 디자인 관련 스타일은 `<head>` 내부의 `<style>` 태그 안에 통합하여 작성하라. 본문(body) 내에서는 가급적 인라인 스타일보다 클래스나 구조적 선택자를 활용하라.
        - **태그**: `</body>` 태그 바로 직전에 `<div id="tags" style="display:none">tag1, tag2, ...</div>` 를 포함하세요.
        - 모든 결과물은 브라우저에서 바로 열었을 때 완벽하게 렌더링되어야 한다.

        **주제**: {topic}
        **날짜**: {datetime.now().strftime('%Y-%m-%d')}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category='HARM_CATEGORY_HATE_SPEECH',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_HARASSMENT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARM_CATEGORY_DANGEROUS_CONTENT',
                            threshold='BLOCK_NONE'
                        ),
                    ]
                )
            )
            
            if not response.text:
                if response.candidates:
                    print(f"--- [DEBUG] Finish Reason: {response.candidates[0].finish_reason} ---")
                return None
                
            return response.text
        except Exception as e:
            print(f"\n--- 콘텐츠 생성 중 오류 발생 ---")
            print(f"Error: {e}")
            return None

    def extract_tags(self, html_content):
        """
        숨겨진 div 및 본문 내 해시태그에서 태그를 추출합니다.
        """
        tags = []
        # 1. 숨겨진 Div
        match = re.search(r'<div id="tags"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        if match:
            tags_str = match.group(1)
            for t in tags_str.split(','):
                tag = t.strip()
                if tag and not re.match(r'^[0-9a-fA-F]{3,6}$', tag):
                    tags.append(tag)

        # 2. 해시태그
        hashtags = re.findall(r'(?:^|\s)#(\w+)', html_content)
        for ht in hashtags:
            if not re.match(r'^[0-9a-fA-F]{3,6}$', ht):
                tags.append(ht)

        unique_tags = list(dict.fromkeys([t for t in tags if t]))
        return unique_tags[:20]

    def clean_html(self, html_content):
        cleaned = html_content.strip()
        cleaned = re.sub(r'^```html\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        return cleaned.strip()
