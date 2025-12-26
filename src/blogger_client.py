import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class BloggerClient:
    def __init__(self, client_id, client_secret, refresh_token, blog_id):
        self.blog_id = blog_id
        self.scopes = ['https://www.googleapis.com/auth/blogger']
        
        # 토큰에서 직접 자격 증명 객체 생성
        # 항상 리프레시 토큰이 있다고 가정하고 이를 사용하여 갱신합니다.
        self.creds = Credentials(
            None, # 초기 액세스 토큰 없음
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=self.scopes
        )

    def get_service(self):
        if not self.creds.valid:
            if self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"토큰 갱신 중 오류 발생: {e}")
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
