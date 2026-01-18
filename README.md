```
# Gemini AI & GitHub Actions를 활용한 블로그 자동화

이 프로젝트는 Gemini 2.5 Flash Lite를 사용하여 콘텐츠를 생성하고 GitHub Actions를 사용하여 구글 블로거(Blogger)에 포스팅을 자동화합니다.

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
6.  JSON 파일을 다운로드하여 `client_secrets.json`으로 저장하거나 `클라이언트 ID`와 `클라이언트 보안 비밀`을 복사합니다.

### 2. 리프레시 토큰(Refresh Token) 발급
스크립트가 무인으로 실행되려면 `refresh_token`을 얻는 일회성 과정이 필요합니다.
1. `client_secrets.json` 파일이 프로젝트 루트에 있는지 확인합니다.
2. `get_token.py`를 실행합니다:
   ```bash
   python get_token.py
   ```
3. 브라우저가 열리면 Google 계정으로 로그인하고 권한을 승인합니다.
4. 터미널에 출력된 `리프레시 토큰`을 복사하여 안전한 곳에 보관하세요.

### 3. 환경 변수 (.env) 설정 (로컬 실행용)
로컬에서 테스트하려면 프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 채웁니다:

```env
# Gemini API Key (https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key

# Google Cloud Console OAuth Client Info
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

# 리프레시 토큰 (get_token.py 실행 결과)
REFRESH_TOKEN=your_refresh_token_here

# 블로그 ID (블로그 관리 페이지 URL에서 확인 가능: blogID=...)
BLOG_ID=your_blog_id
```

### 4. GitHub Secrets 설정
GitHub 저장소 -> Settings -> Secrets and variables -> Actions -> New repository secret으로 이동합니다.
다음 비밀(Secret)들을 추가하세요:

- `GEMINI_API_KEY`: Gemini API 키.
- `CLIENT_ID`: Cloud Console에서 확인한 값.
- `CLIENT_SECRET`: Cloud Console에서 확인한 값.
- `REFRESH_TOKEN`: 방금 얻은 토큰.
- `BLOG_ID`: 블로그 관리 페이지 URL에서 찾을 수 있는 Blog ID.

### 5. 직접 실행
로컬에서 실행하려면:
1.  `.env` 파일을 생성하고 값을 채웁니다.
2.  `pip install -r requirements.txt`를 실행합니다.
3.  `python main.py "원하는 주제"`를 실행합니다. 주제를 입력하지 않으면 AI가 자동으로 추천합니다.

## 주요 기능
- **신중한 역발상 투자자 페르소나**: 투자 중심 콘텐츠.
- **서버리스**: GitHub Actions에서 실행됩니다.
- **자동 태그 지정**: 라벨용 키워드를 자동 추출합니다.
- **초안 모드**: 안전을 위해 초안으로 업로드합니다.
```
