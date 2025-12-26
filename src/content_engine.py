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
    def generate_content(self, topic):
        """
        [투자분석 블로그 통합 프롬프트 시스템 v3.0]과 사용자 지정 스타일 가이드가 결합된 프롬프트를 사용합니다.
        """
        prompt = f"""
        당신은 20년 경력의 가치 투자 분석가입니다. 이번 분석 주제는 **"{topic}"** 입니다. 
        아래의 **[스타일 가이드]**와 **[v3.0 통합 시스템]** 사양을 결합하여 최상의 블로그 포스트를 작성하세요.

        ---

        ## 목차

1. [시스템 개요](https://www.notion.so/2d57fc9ecd4f80da969fe47dc262230c?pvs=21)
2. [Layer 1: Design System Foundation](https://www.notion.so/2d57fc9ecd4f80da969fe47dc262230c?pvs=21)
3. [Layer 2: HTML Structure Framework](https://www.notion.so/2d57fc9ecd4f80da969fe47dc262230c?pvs=21)
4. [Layer 3: Content Generation Engine](https://www.notion.so/2d57fc9ecd4f80da969fe47dc262230c?pvs=21)

1. [통합 실행 매뉴얼](https://www.notion.so/2d57fc9ecd4f80da969fe47dc262230c?pvs=21)

---

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
> 

### 📐 디자인 3대 원칙

1. **Minimal Complexity**: 복잡한 금융 정보를 단순하고 명확하게
2. **Data-First Hierarchy**: 데이터가 주인공, 디자인은 조연
3. **Trust Through Consistency**: 일관성으로 전문성 구축

### 🎨 색상 철학

- **Primary (네이비/블루)**: 신뢰와 안정성
- **Semantic (그린/레드)**: 직관적 정보 전달
- **Neutral (그레이)**: 정보 계층 구분
- **원칙**: 5개 이하 주요 색상

### ✍️ 타이포그래피 원칙

- **가독성 우선**: 본문 16px+, 행간 1.75
- **숫자 전용**: 금융 데이터는 고정폭 폰트
- **계층 명확성**: 제목:부제:본문 = 2:1.5:1

### 1.2 CSS 변수 체계

### 색상 시스템

```css
:root {
  /* Primary Colors */
  --color-primary: #1A1A2E;         /* 다크 네이비 */
  --color-secondary: #0F4C75;       /* 딥 블루 */

  /* Semantic Colors */
  --color-accent-positive: #16C79A; /* 상승 */
  --color-accent-negative: #FF6B6B; /* 하락 */

  /* Neutral Colors */
  --color-background: #FFFFFF;
  --color-text-primary: #2C3E50;
}

```

### 타이포그래피 시스템

```css
:root {
  /* Font Stack */
  --font-primary: -apple-system, "Noto Sans KR", sans-serif;
  --font-mono: "SF Mono", Monaco, monospace;

  /* Font Sizes */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.5rem;     /* 24px */
}

```

### 1.3 컴포넌트 정의

### 핵심 컴포넌트 목록

- `.tst-stock-info` - 종목 정보 헤더
- `.key-points-list` - 핵심 포인트 리스트
- `.rating` - 투자 등급 배지
- `.tst-financial-table` - 재무 테이블
- `.trend-{up|down|neutral}` - 트렌드 인디케이터
- `.metric-card` - 지표 카드

---

## Layer 2: HTML Structure Framework

### 2.1 구조 설계 철학

### 🏗️ 기본 기조

> "플랫폼 제약 속의 최대 자유" - 티스토리 한계를 극복하는 창의적 구조
> 

### 📋 구조 설계 4대 원칙

1. **Platform Awareness**
    - 스킨 시스템 충돌 방지
    - 에디터 자동 변환 대응
2. **Performance First**
    - 3초 이내 로딩 목표
    - 이미지 최적화 필수
3. **Reader Centric**
    - 정보 전달 최우선
    - 과도한 장식 배제
4. **Regulatory Compliance**
    - 면책조항 필수 포함
    - 투자권유 오해 방지

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

### 2.3 티스토리 제약사항 대응

### ⚠️ 필수 금지사항

| 항목 | 이유 | 대안 |
| --- | --- | --- |
| `!important` 남용 | 스킨 충돌 | 특정성 높은 선택자 |
| 전역 선택자 | 페이지 영향 | `.tst-` 접두사 |
| `<script>` 태그 | 보안 제거 | 순수 CSS |
| 고정 픽셀값 | 반응형 깨짐 | rem, % 단위 |

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

### 필수 검증 항목

- [ ]  비즈니스 모델 명확화
- [ ]  Porter's Five Forces 평가
- [ ]  대체 불가능성 검증
- [ ]  경영진 트랙레코드
- [ ]  시장점유율 추이

### 데이터 소스 우선순위

**한국 기업**

| 순위 | 소스 | 용도 |
| --- | --- | --- |
| 1순위 | DART | 공시자료 |
| 2순위 | 네이버금융 | 재무제표 |
| 3순위 | 증권사 리서치 | 전문의견 |

**미국 기업**

| 순위 | 소스 | 용도 |
| --- | --- | --- |
| 1순위 | SEC EDGAR | 10-K, 10-Q |
| 2순위 | Yahoo Finance | 실시간 데이터 |
| 3순위 | Bloomberg | 전문 분석 |

### 📈 Stage 2: 재무 건전성 분석

### 3중 검증 시스템

1. **시계열 분석**: 5년 추세
2. **동종업계 비교**: 상대 위치
3. **절대값 평가**: 위험 기준선

### 핵심 지표 체크리스트

**수익성**

- [ ]  ROE > 15%
- [ ]  영업이익률 > 업계평균
- [ ]  FCF Margin > 10%

**안정성**

- [ ]  부채비율 < 100%
- [ ]  유동비율 > 150%
- [ ]  이자보상배율 > 3x

**성장성**

- [ ]  매출 CAGR(3Y) > 10%
- [ ]  EPS 성장률 > 15%

### 🎯 Stage 3: 시나리오 분석

### 확률 가중 시나리오

| 시나리오 | 확률 | 주가영향 |
| --- | --- | --- |
| Bull | 25% | +40~50% |
| Base | 60% | +10~20% |
| Bear | 15% | -20~30% |

### 리스크 매트릭스

```
영향도 →
발생가능성↓   낮음  중간  높음  치명적
매우높음        □    ■    ■     ■
높음           □    □    ■     ■
중간           □    □    □     ■
낮음           □    □    □     □

```

### 💰 Stage 4: 밸류에이션 종합

### DCF 모델 구성

1. 매출 예측 (5년)
2. 비용 구조 분석
3. FCF 도출
4. WACC 산정
5. 터미널 밸류

### 목표주가 도출

```
DCF 가치: 40% 가중
P/E 기준: 20% 가중
P/B 기준: 20% 가중
EV/EBITDA: 20% 가중
─────────────────
종합 목표가 → 안전마진 10% 적용

```

### 🎯 Stage 5: 투자 의사결정

### 투자 매력도 스코어카드 (100점)

- 사업 매력도: 30점
- 재무 건전성: 25점
- 밸류에이션: 25점
- 성장 잠재력: 20점

### 투자의견 기준

```
80-100점: STRONG BUY ★★★★★
60-79점:  BUY ★★★★☆
40-59점:  HOLD ★★★☆☆
20-39점:  SELL ★★☆☆☆
0-19점:   STRONG SELL ★☆☆☆☆

```

### 🔍 Stage 6: 메타인지 검증

### 편향 체크리스트

- [ ]  확증편향 점검
- [ ]  최신성편향 점검
- [ ]  앵커링 점검
- [ ]  과신편향 점검

### 품질 검증 10계명

1. 출처 명확성
2. 논리 일관성
3. 시간축 일치
4. 경쟁사 분석
5. 리스크 고려
6. 독자 관점
7. 이해 가능성
8. 전문성
9. 지속 유효성
10. 투자 가능성

### 3.3 출력 규격

### 📏 섹션별 분량 기준

| 섹션 | 최소 분량 | 필수 요소 |
| --- | --- | --- |
| Summary | 300-500자 | 3줄 요약 |
| 재무분석 | 1,500자+ | 3년 데이터 |
| 밸류에이션 | 1,500자+ | DCF, Multiple |
| 리스크 | 1,000자+ | 매트릭스 |
| 전략 | 800자+ | 진입/출구 |

### 📊 필수 시각화 요소

- 테이블: 5개+
- 차트: 3개+
- 메트릭카드: 4개+
- 트렌드지표: 10개+

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