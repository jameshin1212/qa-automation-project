# 🚀 QUICK START GUIDE

## 5분 안에 테스트 실행하기

### 📋 사전 체크 (30초)
```bash
# 환경 검증 스크립트 실행
python3 setup_validator.py
```

문제가 발견되면 스크립트가 해결 방법을 제시합니다.

---

## 🎯 방법 1: 자동 설정 (권장) - 2분

```bash
# 1. 자동 설정 스크립트 실행
./setup.sh

# 2. 테스트 실행
./run_tests.sh
```

완료! 테스트가 자동으로 실행됩니다.

---

## 🎯 방법 2: Docker 실행 (가장 간단) - 3분

```bash
# 1. Docker 컨테이너 시작
docker-compose up -d

# 2. 테스트 실행
docker-compose run --rm test-runner pytest -v

# 3. 종료
docker-compose down
```

---

## 🎯 방법 3: 수동 설정 - 5분

### Step 1: Python 환경 (1분)
```bash
# Python 3.12 권장
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Mock 서버 설치 (1분)
```bash
cd mock_server
npm install
cd ..
```

### Step 3: Playwright 설치 (1분)
```bash
playwright install webkit
```

### Step 4: Mock 서버 시작 (30초)
```bash
# 새 터미널에서
cd mock_server
npm start
```

### Step 5: 테스트 실행 (1분)
```bash
# 다른 터미널에서
pytest -v
```

---

## ✅ 성공 확인

테스트가 성공적으로 실행되면:
```
======================== test session starts ========================
...
======================== 31 passed in 45.23s ========================
```

---

## 🆘 문제 해결

### Python 버전 오류
```bash
# Python 3.12 설치 (Mac)
brew install python@3.12

# Python 3.12 설치 (Ubuntu)
sudo apt update
sudo apt install python3.12
```

### 포트 3000 사용 중
```bash
# Mac/Linux
kill -9 $(lsof -t -i:3000)

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### 의존성 설치 실패
```bash
# Python 3.13 사용 시
pip install -r requirements-minimal.txt
```

---

## 📊 테스트 리포트 보기

```bash
# Allure 리포트 생성
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 🎬 UI 테스트 관찰하기

브라우저에서 테스트 동작을 보려면:
```bash
pytest tests/ui -v --headed --slowmo=1000
```

---

## 📝 더 자세한 정보

- 전체 문서: [README.md](README.md)
- Python 호환성: [PYTHON_COMPATIBILITY.md](PYTHON_COMPATIBILITY.md)
- 문제 신고: [GitHub Issues](https://github.com/jameshin1212/qa-automation-project/issues)

---

**시작하는 데 문제가 있으신가요?**
`python3 setup_validator.py`를 실행하여 환경을 진단하세요!