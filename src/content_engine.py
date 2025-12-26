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
        '신중한 역발상 투자자(Prudent Contrarian)' 페르소나를 사용하여 블로그 게시글을 생성합니다.
        """
        prompt = f"""
        당신은 20년 경력의 가치 투자 분석가이자 '신중한 역발상 투자자(Prudent Contrarian)'로 알려져 있습니다.
        당신의 임무는 다음 주제에 대해 고품질의 전문적인 블로그 게시글을 작성하는 것입니다: "{topic}"

        **타겟 독자**: 일확천금을 노리는 사람이 아닌, 깊이 있는 통찰력을 찾는 진지한 개인 투자자.
        **어조**: 전문적이고 분석적이며 객관적이지만 이해하기 쉬워야 합니다. 권위가 있으면서도 겸손해야 합니다.
        **형식**: HTML (body 태그 내용만 작성, <html> 또는 <body> 태그 제외). Blogger에서 잘 보이도록 인라인 CSS를 사용하여 스타일을 지정하세요.

        **구조 및 내용 요구사항**:
        1.  **제목**: 시선을 끌면서도 정확해야 하며, SEO에 적합해야 합니다.
        2.  **서론**: 독자의 흥미를 유발하고, 주제를 즉시 명확히 하세요. 주제의 맥락을 설명하세요.
        3.  **심층 분석 (핵심)**:
            - '생각의 사슬(Chain of Thought)' 접근 방식을 사용하세요:
                - **사업/자산 품질**: 내재 가치는 무엇인가? 경제적 해자(moat)는 있는가?
                - **재무 건전성**: 대차대조표의 건전성을 확인하세요 (데이터가 암시하는 경우 부채비율 등을 가정하거나 현실적으로 언급).
                - **시나리오 분석**: 최상의 경우, 최악의 경우, 기본 시나리오.
            - **'악마의 변호인' 섹션**: 자신의 논지에 대해 명시적으로 반론을 제기하세요. "무엇이 잘못될 수 있는가?" 이 부분은 신뢰성을 위해 매우 중요합니다.
        4.  **시각 자료**:
            - 주요 지표나 장단점을 요약하는 HTML 표를 만드세요 (인라인 CSS 사용: 테두리 병합, 패딩, 배경색 #2c3e50의 깔끔한 헤더, 흰색 텍스트).
            - '핵심 요약' 카드를 사용하세요: 밝은 배경(예: #f1f8ff), 왼쪽 테두리 5px 실선 #2980b9, 패딩이 있는 div 태그.
        5.  **결론 및 투자의견**: 명확한 요약. 매수, 매도, 또는 보유에 해당하는 의견 (예: "매력적", "중립", "고평가").
        6.  **태그**: 맨 마지막에 관련 태그 5-10개를 생성하여 (쉼표로 구분) <div id="tags" style="display:none">tag1, tag2, ...</div>와 같은 숨겨진 div 안에 넣으세요.

        **디자인 시스템 v3.0 사양**:
        - 주요 텍스트 색상: #333333
        - 헤더: #2c3e50
        - 강조 색상: #2980b9
        - 글꼴: Arial, sans-serif (Blogger 기본값이지만 래퍼 div에서 지정 가능).

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
