import os
import google.generativeai as genai
import re
from datetime import datetime

class ContentEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # 최신 Gemini 2.0 Flash 모델 사용
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def recommend_topic(self):
        """
        Gemini를 사용하여 최근 10시간 이내에 월가 대부들이 언급하고 레딧에서 화제가 된 기업을 추천받습니다.
        """
        prompt = """
        당신은 금융 시장 트렌드 스카우터입니다.
        다음 조건에 맞는 **단 하나의 상장 기업**을 찾아 추천해주세요. (S&P 500 지수 포함 기업 위주)

        **조건**:
        1. **최근 10시간 이내**에 주요 월가 대부(예: 워런 버핏, 마이클 버리, 레이 달리오, 캐시 우드 등)나 저명한 금융 기관에 의해 언급되거나 뉴스가 나온 기업.
        2. 위 뉴스로 인해 현재 Reddit(WallStreetBets, Stocks 등)이나 소셜 미디어에서 화제가 되고 있는 기업.
        3. **메이저 빅테크 제외**: NVDA, AAPL, MSFT, AMZN, GOOG, TSLA, META 등 이미 너무 유명한 초저명 기업은 제외한다. 오직 해당 기업에 시장에 파괴적인 영향을 줄 만한 대규모 이슈가 발생한 경우에만 예외적으로 추천할 수 있다.

        **결과물**:
        다른 말은 하지 말고, 오직 **기업명(티커)** 만 출력하세요. (예: Ford Motor (F))
        만약 확실한 정보가 없다면, S&P 500 기업 중 현재 시장에서 변동성이 크고 화제가 되는 기업 하나를 선정해 주세요.
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
        [투자분석 블로그 통합 프롬프트 시스템 v3.0]을 생략 없이 온전히 적용하여 콘텐츠를 생성합니다.
        """
        prompt = f"""
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

        ## 시스템 개요
        ### 시스템 아키텍처
        ```
        Layer 1: Design System Foundation (디자인 철학 및 CSS 정의)
            ↓
        Layer 2: HTML Structure Framework (구조 원칙 및 템플릿)
            ↓
        Layer 3: Content Generation Engine (콘텐츠 생성 로직)
        ```
        ### 핵심 목표
        - **신뢰성**: 전문적이고 정확한 투자 정보 제공
        - **일관성**: 통일된 디자인과 구조로 브랜드 구축
        - **효율성**: 재사용 가능한 템플릿과 자동화

        ---

        ## Layer 1: Design System Foundation
        ### 1.1 디자인 철학
        ### 🎨 기본 기조
        > "신뢰를 통한 설득" - 복잡한 금융 정보를 단순하고 명확하게 전달
        ### 📐 디자인 3대 원칙
        1. **Minimal Complexity**: 복잡한 금융 정보를 단순하고 명확하게
        2. **Data-First but easy readable**: 가독성 좋고 긍정/부정이 한눈에 들어오게 함
        3. **Trust Through Consistency**: 일관성으로 전문성 구축
        ### 🎨 색상 철학
        - **Primary (네이비/블루)**: 신뢰와 안정성
        - **Semantic (그린/레드)**: 직관적 정보 전달
        - **Neutral (그레이)**: 정보 계층 구분
        - **원칙**: 5개 이하 주요 색상을 충분히 활용
        ### ✍️ 타이포그래피 원칙
        - **가독성 우선**: 본문 16px+, 행간 1.75
        - **숫자 전용**: 금융 데이터는 고정폭 폰트
        - **계층 명확성**: 제목:부제:본문 = 2:1.5:1

        ### 1.2 CSS 변수 체계
        ### 색상 시스템
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
        ### 타이포그래피 시스템
        ```css
        :root {{
          --font-primary: -apple-system, "Noto Sans KR", sans-serif;
          --font-mono: "SF Mono", Monaco, monospace;
          --text-base: 1rem;     /* 16px */
          --text-lg: 1.125rem;   /* 18px */
          --text-xl: 1.5rem;     /* 24px */
        }}
        ```
        ### 1.3 컴포넌트 정의
        ### 핵심 컴포넌트 목록
        - `.tst-stock-info` - 종목 정보 헤더
        - `.key-points-list` - 핵심 포인트 리스트
        - `.rating` - 투자 등급 배지
        - `.tst-financial-table` - 재무 테이블
        - `.trend-{{up|down|neutral}}` - 트렌드 인디케이터
        - `.metric-card` - 지표 카드

        ---

        ## Layer 2: HTML Structure Framework
        ### 2.1 구조 설계 철학
        ### 📋 구조 설계 4대 원칙
        1. **Platform Awareness**: 스킨 시스템 충돌 방지, 에디터 자동 변환 대응
        2. **Performance First**: 3초 이내 로딩 목표, 이미지 최적화 필수
        3. **Reader Centric**: 가독성 최우선, 적당한 상징색/대비색 활용
        4. **Regulatory Compliance**: 면책조항 필수 포함, 투자권유 오해 방지
        5. **EEAT**: EEAT충족을 위해 다음 내용의 푸터를 넣어주세요. 작성자:우디(Woody), 이력:경제적 자유를 향해 나아가는 5년 차 실전 투자자입니다. AI를 활용해 매일 경제 데이터를 빠르게 수집/분석합니다. 제가 투자자로서 성장해가는 과정을 블로그에 기록하고 있으며, 부족한 정보라도 공유를 통해 인사이트를 얻으실 수 있다면 좋겠습니다. 


        ### 2.2 5-Phase 템플릿 구조
        ```
        Phase 1: Meta Header (메타데이터)
            ├─ 기업 식별 정보
            ├─ 핵심 투자 포인트
            └─ 투자 등급 배지
        Phase 2: Navigation (목차)
            └─ 조건부 자동 생성
        Phase 3: Main Content (본문)
            ├─ Executive Summary
            ├─ 재무 분석
            ├─ 밸류에이션
            └─ 리스크 요인
        Phase 4: Compliance Footer (푸터)
            ├─ 면책조항
            └─ 업데이트 정보
        Phase 5: Inline Styles (스타일)
            └─ 스코프 한정 CSS
        ```

        ---

        ## Layer 3: Content Generation Engine
        ### 3.1 역할 정의
        ### 👤 페르소나
        **'Prudent Contrarian'** - 20년 경력 가치투자 애널리스트
        ### 🧠 3중 사고 모드
        ```
        Primary Mode: 보수적 가치투자자 (자본 보존)
             ↓↑
        Shadow Mode: 성장투자자 관점 (기회비용)
             ↓↑
        Meta Mode: 통합적 지혜
        ```
        ### 3.2 6단계 분석 프레임워크
        ### 📊 Stage 1: 기업 본질 분석
        - 비즈니스 모델 명확화, Porter's Five Forces 평가, 대체 불가능성 검증, 경영진 트랙레코드, 시장점유율 추이
        ### 📈 Stage 2: 재무 건전성 분석
        - 3중 검증 시스템 (시계열 분석, 동종업계 비교, 절대값 평가)
        - 핵심 지표: ROE > 15%, 영업이익률 > 업계평균, FCF Margin > 10%, 부채비율 < 100%, 유동비율 > 150%, 이자보상배율 > 3x, 매출 CAGR(3Y) > 10%, EPS 성장률 > 15%
        ### 🎯 Stage 3: 시나리오 분석
        - 확률 가중 시나리오: Bull(25%, +40~50%), Base(60%, +10~20%), Bear(15%, -20~30%)
        - 리스크 매트릭스 활용
        ### 💰 Stage 4: 밸류에이션 종합
        - DCF 모델 구성 (매출 예측, 비용 구조, FCF, WACC, 터미널 밸류)
        - 목표주가 도출: DCF(40%), P/E(20%), P/B(20%), EV/EBITDA(20%) 가중치 적용 및 안전마진 10% 적용
        ### 🎯 Stage 5: 투자 의사결정
        - 투자 매력도 스코어카드 (100점 만점): 사업(30), 재무(25), 밸류(25), 성장(20)
        - 투자의견: STRONG BUY(80-100), BUY(60-79), HOLD(40-59), SELL(20-39), STRONG SELL(0-19)
        ### 🔍 Stage 6: 메타인지 검증
        - 편향 점검 (확증, 최신성, 앵커링, 과신) 및 품질 검증 10계명 준수

        ### 3.3 출력 규격
        ### 📏 섹션별 분량 기준
        - Summary: 300-500자
        - 재무분석: 1,500자+
        - 밸류에이션: 1,500자+
        - 리스크: 1,000자+
        - 전략: 800자+
        ### 📊 필수 시각화 요소
        - 테이블: 3개+
        - 차트: 1개+
        - 메트릭카드: 2개+
        - 트렌드지표: 1개+

        ---

        **형식 요구사항**:
        - 출력 형식: HTML (body 내용만 작성, <html> 또는 <body> 태그 제외)
        - **태그**: 맨 마지막에 <div id="tags" style="display:none">tag1, tag2, ...</div>와 같은 숨겨진 div 안에 관련 태그 10-20개를 넣으세요.

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
