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
        '투자분석 블로그 티스토리 통합 프롬프트 시스템 v3.0'을 사용하여 콘텐츠를 생성합니다.
        """
        prompt = f"""
        당신은 20년 경력의 가치 투자 분석가이자 '신중한 역발상 투자자(Prudent Contrarian)'입니다.
        이번 분석 주제는 **"{topic}"** 입니다. 
        다음의 **[투자분석 블로그 통합 프롬프트 시스템 v3.0]** 사양을 엄격히 준수하여 고품질의 블로그 포스트를 작성하세요.

        ---

        ### Layer 1: Design System Foundation (CSS & Components)
        - **디자인 철학**: "신뢰를 통한 설득" - 복잡한 정보를 단순하고 명확하게 전달.
        - **색상 체계 (Inline CSS 필수)**:
            - Primary: #1A1A2E (다크 네이비 / 헤더 배경)
            - Secondary: #0F4C75 (딥 블루)
            - Accent Positive: #16C79A (상승/긍정)
            - Accent Negative: #FF6B6B (하락/부정)
            - Background: #FFFFFF / Text: #2C3E50
        - **컴포넌트**:
            - `.tst-stock-info`: 종목 정보 헤더 (배경 #1A1A2E, 흰색 텍스트)
            - `.metric-card`: 지표 카드 (옅은 배경, 왼쪽 강조 테두리 #0F4C75)
            - `.tst-financial-table`: 깔끔한 테두리와 헤더를 가진 재무 테이블

        ### Layer 2: HTML Structure Framework (5-Phase Template)
        1. **Phase 1: Meta Header**: 기업 식별 정보, 3줄 핵심 투자 포인트, 별점 투자 등급 배지.
        2. **Phase 2: Navigation**: 분석 목차 (앵커 포함).
        3. **Phase 3: Main Content**:
            - **Executive Summary**: 개괄적 요약.
            - **재무 분석**: 3년 시계열 데이터 포함 테이블.
            - **밸류에이션**: DCF 또는 Multiple 분석 모델 기반 목표가 도출.
            - **리스크 요인**: '악마의 변호인' 관점에서의 리스크 매트릭스.
        4. **Phase 4: Compliance Footer**: 강력한 면책조항 (본 글은 투자를 권유하지 않으며... 등).
        5. **Phase 5: Inline Styles**: 모든 스타일은 태그의 `style` 속성에 직접 작성.

        ### Layer 3: Content Generation Engine (6-Stage Framework)
        - **Stage 1: 기업 본질**: 비즈니스 모델, 경제적 해자, 시장 점유율.
        - **Stage 2: 재무 건전성**: ROE, 영업이익률, 부채비율, FCF 분석.
        - **Stage 3: 시나리오**: Bull/Base/Bear 확률 가중 시나리오 분석.
        - **Stage 4: 밸류에이션**: 안전마진 10%를 적용한 종합 목표주가 도출.
        - **Stage 5: 의사결정**: STRONG BUY부터 STRONG SELL까지 명확한 의견.
        - **Stage 6: 메타인지**: 스스로의 확증 편향 및 최신성 편향을 점검하고 보수적으로 접근.

        ---

        **출력 규격**:
        - 형식: HTML (body 내용만, <body> 태그 제외)
        - 시각화: 최소 3개 이상의 데이터 테이블, 5개 이상의 강조 카드(`div`) 포함.
        - 분량: 전문적이고 깊이 있는 분석 (최소 1,500자 이상).
        - 언어: 한국어
        - **태그**: 맨 마지막에 관련 태그 5-10개를 <div id="tags" style="display:none">tag1, tag2, ...</div> 안에 쉼표로 구분하여 포함하세요.

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
