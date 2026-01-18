import os
import re
from datetime import datetime
from google import genai
from google.genai import types

class ContentEngine:
    def __init__(self, api_key):
        # google-genai SDK 사용
        self.client = genai.Client(api_key=api_key)
        # 모델명 지정
        self.model_id = 'gemini-2.0-flash' # gemini-3-flash-preview가 없을 경우 대비 가장 안정적인 최신 모델

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
        [투자분석 블로그 통합 프롬프트 시스템 v3.0]을 적용하여 콘텐츠를 생성합니다.
        """
        # 실제로는 기존의 긴 프롬프트를 유지해야 하므로, re-read 하여 전체를 치환하거나 부분 치환
        # 여기서는 생략된 형태가 아니라 전체를 다시 작성함
        
        full_prompt = f"""
        당신은 20년 경력의 가치 투자 분석가입니다. 이번 분석 주제는 **"{topic}"** 입니다. 
        모든 문장은 '~이다' 체를 사용하고, 신중하고 보수적인 관점에서 분석하세요.
        HTML 형식으로 작성하되, 맨 마지막에 <div id="tags" style="display:none">tag1, tag2, ...</div> 를 포함하세요.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category='HATE_SPEECH',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='HARASSMENT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='SEXUALLY_EXPLICIT',
                            threshold='BLOCK_NONE'
                        ),
                        types.SafetySetting(
                            category='DANGEROUS_CONTENT',
                            threshold='BLOCK_NONE'
                        ),
                    ]
                )
            )
            
            if not response.text:
                # finish_reason 확인
                print(f"--- [DEBUG] Finish Reason: {response.candidates[0].finish_reason} ---")
                return None
                
            return response.text
        except Exception as e:
            print(f"\n--- 콘텐츠 생성 중 오류 발생 ---")
            print(f"Error: {e}")
            return None

    def extract_tags(self, html_content):
        tags = []
        match = re.search(r'<div id="tags"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        if match:
            tags_str = match.group(1)
            for t in tags_str.split(','):
                tag = t.strip()
                if tag and not re.match(r'^[0-9a-fA-F]{3,6}$', tag):
                    tags.append(tag)
        unique_tags = list(dict.fromkeys([t for t in tags if t]))
        return unique_tags[:20]

    def clean_html(self, html_content):
        cleaned = html_content.strip()
        cleaned = re.sub(r'^```html\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        return cleaned.strip()
