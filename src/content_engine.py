import os
import google.generativeai as genai
import re
from datetime import datetime

class ContentEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # 사용 가능한 모델 목록에 따라 Flash 최신 버전으로 업데이트
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def recommend_topic(self):
        """
        Gemini를 사용하여 최근 10시간 이내에 월가 대부들이 언급하고 레딧에서 화제가 된 기업을 추천받습니다.
        """
        prompt = """
        당신은 금융 시장 트렌드 스카우터입니다.
        다음 조건에 맞는 **단 하나의 상장 기업**을 찾아 추천해주세요.

        **조건**:
        1. **최근 10시간 이내**에 주요 월가 대부(예: 워런 버핏, 마이클 버리, 레이 달리오, 캐시 우드 등)나 저명한 금융 기관에 의해 언급되거나 뉴스가 나온 기업.
        2. 위 뉴스로 인해 현재 Reddit(WallStreetBets, Stocks 등)이나 소셜 미디어에서 화제가 되고 있는 기업.

        **결과물**:
        다른 말은 하지 말고, 오직 **기업명(티커)** 만 출력하세요. (예: Tesla (TSLA))
        만약 확실한 정보가 없다면, 현재 시장에서 가장 변동성이 크고 화제가 되는 기술주 하나를 선정해 주세요.
        """
        try:
            response = self.model.generate_content(prompt)
            # 불필요한 공백이나 마침표 제거
            topic = response.text.strip()
            return topic
        except Exception as e:
            print(f"주제 추천 중 오류 발생: {e}")
            return "NVIDIA (NVDA)" # 오류 시 기본값

    def generate_content(self, topic):
        """
        사용자 지정 스타일 가이드가 적용된 v3.0 프롬프트 시스템을 사용하여 콘텐츠를 생성합니다.
        """
        prompt = f"""
        당신은 20년 경력의 가치 투자 분석가입니다. 이번 분석 주제는 **"{topic}"** 입니다. 
        다음의 지침을 엄격히 준수하여 전문적인 블로그 포스트를 작성하세요.

        ---

        ### ✍️ 스타일 가이드 (가장 중요)
        1. **문체**: 모든 문장은 기본적으로 **'~이다'** 체(평서문)를 사용하세요.
        2. **사견 및 통찰**: 글의 중간중간 당신의 주관적인 사견을 포함하세요. 이는 불확실한 인사이트여도 괜찮습니다.
           - 문체는 "문득 이런 생각이 든다...", "글쎄, 내 생각에는...", "개인적으로는 이 지점이 의심스럽다"와 같이 **혼잣말 같은 자연스러운 어투**를 사용하여 사견임을 드러내세요.
        3. **페르소나 언급 금지**: 본문에서 "나는 신중한 역발상 투자자이다"와 같이 자신의 정체성을 직접적으로 밝히지 마세요. 분석의 깊이로 정체성을 증명하세요.
        4. **투자의견 조절**: 의견을 너무 강요하거나 확정적으로 말하지 말고, **신중하고 보수적인 관점**에서 부드럽게 표현하세요.
        5. **영문 병기 금지**: 괄호 안에 불필요한 영문 번역 명칭(예: 가치투자(Value Investing))을 넣지 마세요. 꼭 필요한 경우를 제외하고는 한국어만 사용합니다.
        6. **용어 사용 주의**: '악마의 변호인'이라는 단어를 본문에 직접적으로 노출하지 마세요. 대신 리스크 분석, 반론, 혹은 고려해야 할 위험 요소 등으로 자연스럽게 표현하세요.

        ---

        ### Layer 1: Design System Foundation (Inline CSS)
        - Primary: #1A1A2E (네이비), Secondary: #0F4C75 (딥 블루)
        - Accent Positive: #16C79A, Accent Negative: #FF6B6B
        - 모든 디자인 요소는 태그 내 `style` 속성으로 구현하세요.

        ### Layer 2: HTML Structure (5-Phase)
        1. **Meta Header**: 기업 정보, 3줄 핵심 포인트, 투자 등급(별점).
        2. **Navigation**: 주요 섹션 목차.
        3. **Main Content**:
           - **Executive Summary**: 개요.
           - **재무 분석**: 3개년 시계열 테이블 필수.
           - **밸류에이션**: 목표주가 산출 과정 (안전마진 10% 적용).
           - **리스크 분석**: 리스크 매트릭스 포함.
        4. **Compliance Footer**: 면책조항 필수.

        ### Layer 3: Content Framework (6-Stage)
        - 기업의 본질, 재무 건전성, 시나리오 분석, 신중한 의사결정 과정을 단계별로 서술하되 위 스타일 가이드를 준수하세요.

        ---

        **출력 규격**:
        - 형식: HTML (body 내용만, <body> 태그 제외)
        - 시각화: 데이터 테이블 3개 이상, 강조 카드 5개 이상.
        - 분량: 1,500자 이상의 깊이 있는 분석.
        - **태그**: 맨 마지막에 <div id="tags" style="display:none">tag1, tag2, ...</div> 포함.

        **주제**: {topic}
        **날짜**: {datetime.now().strftime('%Y-%m-%d')}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"콘텐츠 생성 중 오류 발생: {e}")
            return None

    def extract_tags(self, html_content):
        """
        숨겨진 div에서 태그를 추출하고, 본문 내의 해시태그(#Keyword)도 감지하여 라벨로 추출합니다.
        CSS 색상 코드(예: #ffffff, #333)는 제외합니다.
        """
        tags = []
        import re

        # 1. 숨겨진 Div에서 태그 추출 (기존 로직)
        match = re.search(r'<div id="tags"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        if match:
            tags_str = match.group(1)
            # 깔끔하게 정리하며 추가
            for t in tags_str.split(','):
                tag = t.strip()
                if tag and not re.match(r'^[0-9a-fA-F]{3,6}$', tag):
                    tags.append(tag)

        # 2. 본문 내 해시태그 추출 (예: #반도체 #투자)
        # 헥사 코드 형식(#ffffff)은 제외하기 위해 앞에 공백이나 시작점이 있고 뒤에 문자가 오는 패턴 사용
        hashtags = re.findall(r'(?:^|\s)#(\w+)', html_content)
        for ht in hashtags:
            # 숫자로만 이루어진 3자리 또는 6자리 (색상 코드 가능성) 제외
            if not re.match(r'^[0-9a-fA-F]{3,6}$', ht):
                tags.append(ht)

        # 중복 제거 및 빈 문자열 제거
        unique_tags = list(dict.fromkeys([t for t in tags if t]))
        
        # Blogger API 라벨 제한 (보통 20개 내외가 안전)
        return unique_tags[:20]

    def clean_html(self, html_content):
        """
        마크다운 코드 블록이나 불필요한 공백을 정리합니다.
        """
        cleaned = html_content.strip()
        # 마크다운 코드 블록 제거
        cleaned = re.sub(r'^```html\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        return cleaned.strip()
