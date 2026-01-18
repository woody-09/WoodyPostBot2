import os
import re
from datetime import datetime
from google import genai
from google.genai import types

class ContentEngine:
    def __init__(self, api_key):
        # google-genai SDK 사용
        self.client = genai.Client(api_key=api_key)
        # 호출 우선순위 모델 리스트
        self.models = ['gemini-3-flash', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']

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
        
        for model in self.models:
            try:
                print(f"--- 주제 추천 시도 중: {model} ---")
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7
                    )
                )
                if response.text:
                    return response.text.strip()
                else:
                    raise ValueError("Response text is empty")
            except Exception as e:
                err_msg = str(e)
                if "404" in err_msg or "429" in err_msg or "NotFound" in err_msg or "TooManyRequests" in err_msg:
                    print(f"--- {model} 실패 (에러: {err_msg}). 다음 모델 시도 ---")
                    continue
                else:
                    print(f"--- {model} 예상치 못한 오류 발생: {e} ---")
                    break
        
        print("--- 모든 모델 호출 실패. 기본값 반환 ---")
        return "NVIDIA (NVDA)"

    def generate_content(self, topic):
        """
        [투자분석 블로그 통합 프롬프트 시스템 v3.0]을 온전히 적용하여 콘텐츠를 생성합니다.
        """
        full_prompt = f"""
[투자분석 블로그 통합 프롬프트 시스템 v3.0]을 온전히 적용하여 다음 주제에 대한 전문적인 분석 리포트를 작성하십시오.

---

## 2. Layer 1: Advanced Design System

### 2.3 디자인 가이드라인 (Design System Reference)
```css
:root {{
  /* Font Stack */
  --font-primary: -apple-system, "Noto Sans KR", sans-serif;
  --font-mono: "SF Mono", Monaco, monospace;
  
  /* Font Sizes */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.5rem;     /* 24px */
}}
```

### 2.4 컴포넌트 정의
- `.tst-stock-info` - 종목 정보 헤더
- `.key-points-list` - 핵심 포인트 리스트
- `.rating` - 투자 등급 배지
- `.tst-financial-table` - 재무 테이블
- `.trend-{{up|down|neutral}}` - 트렌드 인디케이터
- `.metric-card` - 지표 카드

---

## 3. Layer 2: HTML Structure Framework

### 3.1 구조 설계 철학

#### 📋 구조 설계 4대 원칙
1. **Platform Awareness**
   - 스킨 시스템 충돌 방지
   - 에디터 자동 변환 대응

2. **EEAT 준수**
   - 작성자 푸터 포함 (작성자: 우디(Woody), 실전 투자 분석가)
   - 면책조항 필수 포함

### 3.2 5-Phase 템플릿 구조
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

### 3.3 티스토리 및 블로거 제약사항 대응

#### ⚠️ 필수 금지사항
| 항목 | 이유 | 대안 |
|------|------|------|
| `!important` 남용 | 스킨 충돌 | 특정성 높은 선택자 |
| 전역 선택자 | 페이지 영향 | `.tst-` 접두사 |
| `<script>` 태그 | 보안 제거 | 순수 CSS |
| 고정 픽셀값 | 반응형 깨짐 | rem, % 단위 |

### 3.4 HTML 형식 요구사항 (Blogger 최적화)

#### 📋 필수 준수사항
1. **HTML 구조**
   - `<body>` 태그 내의 콘텐츠만 작성
   - `<html>`, `<head>`, `<body>` 태그는 작성하지 않음

2. **CSS 처리 (Inline CSS ONLY)**
   - 모든 스타일은 각 태그 내의 **인라인 'style' 속성**으로만 작성
   - `<head>` 내의 `<style>` 태그 사용 **절대 금지**
   - 모든 스타일 선언은 개별 요소에 직접 적용

3. **제약 사항**
   - JavaScript (`<script>`) 사용 금지
   - 외부 iFrame 사용 금지
   - Deprecated 태그 및 속성 사용 금지 (`bgcolor`, `font`, `center` 등)
   - 모든 스타일링은 CSS를 활용

---

## 4. Layer 3: Content Generation Engine

### 4.1 역할 정의

#### 👤 페르소나
**'Prudent Contrarian'** - 20년 경력 가치투자 애널리스트

#### 🧠 3중 사고 모드
```
Primary Mode: 보수적 가치투자자 (자본 보존)
     ↓↑
Shadow Mode: 성장투자자 관점 (기회비용)
     ↓↑
Meta Mode: 통합적 지혜
```

### 4.2 콘텐츠 내용
- 사용자가 입력한 주제를 기반으로 전문적인 데이터 분석 및 통찰을 제공

### 4.3 출력 규격

#### 📏 섹션별 분량 기준
| 섹션 | 최소 분량 | 필수 요소 |
|------|----------|----------|
| Summary | 300-500자 | 3줄 요약 |
| 재무분석 | 1,500자+ | 3년 데이터 |
| 밸류에이션 | 1,500자+ | DCF, Multiple |
| 리스크 | 1,000자+ | 매트릭스 |
| 전략 | 800자+ | 진입/출구 |

#### 📊 필수 시각화 요소
- 테이블: 5개+
- 차트: 3개+ (HTML/CSS로 구현)
- 메트릭카드: 4개+
- 트렌드지표: 10개+

---

## 5. 통합 실행 매뉴얼

### 5.1 Phase 1: 준비 (Preparation)
```
□ 기업 선정 및 티커 확인
□ 3개년 재무제표 수집
□ 경쟁사 3개 선정
□ 최근 공시/뉴스 수집
```

### 5.2 Phase 2: 실행 (Execution)
```
□ Layer 1: 디자인 시스템 적용 (인라인 스타일링)
□ Layer 2: HTML 구조 생성
□ Layer 3: 6단계 정밀 분석 실행
□ 데이터 검증
```

### 5.3 Phase 3: 검증 (Validation)
```
□ 기술 검증 (HTML/CSS 호환성)
□ 콘텐츠 검증 (정확성 및 EEAT)
□ 품질 검증 (가독성 및 편집디자인)
□ 법무 검증 (면책조항 포함)
```

**주제**: {topic}
**날짜**: {datetime.now().strftime('%Y-%m-%d')}
**결과물 언어**: 한국어
"""

        for model in self.models:
            try:
                print(f"--- 콘텐츠 생성 시도 중: {model} ---")
                response = self.client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
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
                    raise ValueError("Response text is empty")
                    
                return response.text
            except Exception as e:
                err_msg = str(e)
                if "404" in err_msg or "429" in err_msg or "NotFound" in err_msg or "TooManyRequests" in err_msg:
                    print(f"--- {model} 실패 (에러: {err_msg}). 다음 모델 시도 ---")
                    continue
                else:
                    print(f"--- {model} 예상치 못한 오류 발생: {e} ---")
                    break
        
        print("--- 모든 모델 호출 실패 ---")
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
