# Gemini AI & GitHub Actions를 활용한 블로그 자동화

이 프로젝트는 Gemini 3 flash를 사용하여 콘텐츠를 생성하고 GitHub Actions를 사용하여 구글 블로거(Blogger)에 포스팅을 자동화합니다.

## 전제 조건

1.  **Google 계정** (Blogger 및 Cloud Console 용).
2.  **Gemini API 키** (Google AI Studio에서 발급).
3.  **GitHub 계정** (저장소 호스팅 및 Actions 실행 용).

## 설정 가이드

### 1. Google Cloud Console 설정 (Blogger API)
1.  [Google Cloud Console](https://console.cloud.google.com/)로 이동합니다.
2.  새 프로젝트를 만듭니다.
3.  **Blogger API v3**를 활성화합니다.
4.  **사용자 인증 정보** -> **사용자 인증 정보 만들기** -> **OAuth 클라이언트 ID**로 이동합니다.
5.  애플리케이션 유형: **데스크톱 앱** (초기 리프레시 토큰을 얻기에 가장 쉽습니다).
6.  JSON 파일을 다운로드하거나 `클라이언트 ID`와 `클라이언트 보안 비밀`을 복사합니다.

### 2. 리프레시 토큰(Refresh Token) 발급
스크립트가 무인으로 실행되려면 `refresh_token`을 얻는 일회성 과정이 필요합니다.
제공된 헬퍼 스크립트를 실행하세요 (로컬에서 임시로 파일을 생성하거나 Postman 같은 도구를 사용할 수 있지만, 로컬 스크립트가 가장 쉽습니다):

```python
# 'get_token.py'라는 이름으로 파일 생성
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/blogger']
CLIENT_CONFIG = {
    "installed": {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
creds = flow.run_local_server(port=0)

print("Refresh Token:", creds.refresh_token)
```
이 스크립트를 로컬에서 실행하고 Google 계정으로 로그인한 후, 콘솔에 출력된 `Refresh Token`을 복사하세요.

### 3. GitHub Secrets 설정
GitHub 저장소 -> Settings -> Secrets and variables -> Actions -> New repository secret으로 이동합니다.
다음 비밀(Secret)들을 추가하세요:

- `GEMINI_API_KEY`: Gemini API 키.
- `CLIENT_ID`: Cloud Console에서 확인한 값.
- `CLIENT_SECRET`: Cloud Console에서 확인한 값.
- `REFRESH_TOKEN`: 방금 얻은 토큰.
- `BLOG_ID`: 블로거 설정 페이지 URL에서 찾을 수 있는 Blog ID.

### 4. 직접 실행
로컬에서 테스트하려면:
1.  `.env.example`을 `.env`로 복사하고 값을 채웁니다.
2.  `pip install -r requirements.txt`를 실행합니다.
3.  `python main.py "원하는 주제"`를 실행합니다.

## 주요 기능
- **신중한 역발상 투자자 페르소나**: 투자 중심 콘텐츠.
- **서버리스**: GitHub Actions에서 실행됩니다.
- **자동 태그 지정**: 라벨용 키워드를 자동 추출합니다.
- **초안 모드**: 안전을 위해 초안으로 업로드합니다.
