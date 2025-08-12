# Python 버전 호환성 가이드

## 🔴 Python 3.13 호환성 문제

Python 3.13 (2024년 10월 출시)과 일부 패키지의 호환성 문제가 있습니다:

### 문제가 있는 패키지들:
- **pandas 2.1.4**: C 확장 컴파일 오류
- **greenlet 3.0.1**: Playwright 의존성, C++ 컴파일 오류

## ✅ 해결 방법

### 방법 1: Python 3.12 사용 (권장) ⭐
```bash
# macOS (Homebrew)
brew install python@3.12

# Python 3.12로 가상환경 생성
python3.12 -m venv venv
source venv/bin/activate

# 모든 패키지 설치
pip install -r requirements.txt
playwright install webkit
```

### 방법 2: API 테스트만 사용 (Python 3.13 가능)
```bash
# Python 3.13 사용 시
python3.13 -m venv venv
source venv/bin/activate

# API 테스트용 패키지만 설치
pip install -r requirements-api-only.txt
```

### 방법 3: Docker 사용 (모든 테스트 가능)
```bash
# Python 버전 관계없이 Docker로 실행
docker-compose up -d mock-server
docker-compose run --rm test-runner pytest tests/api -v
docker-compose run --rm test-runner pytest tests/ui -v
```

## 📊 Python 버전별 호환성 표

| Python 버전 | API 테스트 | UI 테스트 | Excel 생성 | 권장도 |
|------------|-----------|-----------|-----------|--------|
| 3.8        | ✅        | ✅        | ✅        | ⭐⭐⭐  |
| 3.9        | ✅        | ✅        | ✅        | ⭐⭐⭐  |
| 3.10       | ✅        | ✅        | ✅        | ⭐⭐⭐⭐ |
| 3.11       | ✅        | ✅        | ✅        | ⭐⭐⭐⭐ |
| 3.12       | ✅        | ✅        | ✅        | ⭐⭐⭐⭐⭐ |
| 3.13       | ✅        | ❌        | ❌        | ⭐⭐    |

## 🚀 빠른 시작 가이드

### Python 3.12 설치 및 프로젝트 실행
```bash
# 1. Python 3.12 설치
brew install python@3.12

# 2. 프로젝트 클론
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project

# 3. 가상환경 생성 및 활성화
python3.12 -m venv venv
source venv/bin/activate

# 4. 패키지 설치
pip install -r requirements.txt

# 5. Playwright 브라우저 설치
playwright install webkit

# 6. Mock 서버 설치
cd mock_server
npm install
cd ..

# 7. 테스트 실행
# 터미널 1: Mock 서버 실행
cd mock_server && npm start

# 터미널 2: 테스트 실행
pytest tests/api -v  # API 테스트
pytest tests/ui -v   # UI 테스트
```

## 🐳 Docker 사용 (Python 버전 무관)

Python 버전과 관계없이 Docker를 사용하면 모든 테스트를 실행할 수 있습니다:

```bash
# Docker Compose로 실행
docker-compose up -d mock-server
docker-compose run --rm test-runner pytest -v
```

## 📝 참고사항

- **API 테스트**: 모든 Python 버전에서 정상 작동
- **UI 테스트**: Python 3.13에서는 greenlet 컴파일 문제로 사용 불가
- **Excel 문서 생성**: Python 3.13에서는 pandas 호환성 문제로 사용 불가
- **Docker**: Python 버전과 무관하게 모든 기능 사용 가능