# 🐳 Docker Quick Start Guide

## 환경 독립적인 테스트 실행 - 3분 완료!

Docker를 사용하면 Python 버전이나 의존성 충돌 걱정 없이 테스트를 실행할 수 있습니다.

---

## 📋 사전 요구사항

Docker Desktop이 설치되어 있어야 합니다:
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker for Linux](https://docs.docker.com/engine/install/)

설치 확인:
```bash
docker --version
docker-compose --version
```

---

## 🚀 빠른 시작 (1분)

### 1. 프로젝트 클론
```bash
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project
```

### 2. Docker로 테스트 실행
```bash
# 모든 테스트 실행 (Mock 서버 + 테스트)
docker-compose up qa-test
```

끝! 테스트가 자동으로 실행됩니다.

---

## 📊 테스트 옵션

### API 테스트만 실행
```bash
docker-compose run --rm qa-test bash -c "cd mock_server && npm start & sleep 5 && pytest tests/api -v"
```

### UI 테스트만 실행
```bash
docker-compose run --rm qa-test bash -c "cd mock_server && npm start & sleep 5 && pytest tests/ui -v"
```

### Smoke 테스트 실행
```bash
docker-compose run --rm qa-test bash -c "cd mock_server && npm start & sleep 5 && pytest -m smoke -v"
```

---

## 🎯 개발 모드 (Mock 서버와 테스트 분리)

### Mock 서버만 실행
```bash
docker-compose --profile dev up mock-server
```

### 테스트만 실행 (Mock 서버가 이미 실행 중일 때)
```bash
docker-compose --profile dev run --rm test-runner
```

---

## 📈 Allure Report 보기

테스트 실행 후 리포트 확인:
```bash
# 로컬에서 Allure 리포트 서버 시작
docker run -p 5050:5050 -v $(pwd)/allure-results:/app/allure-results frankescobar/allure-docker-service
```

브라우저에서 http://localhost:5050 접속

---

## 🧹 정리

### 컨테이너 정지 및 삭제
```bash
docker-compose down
```

### 이미지까지 완전 삭제
```bash
docker-compose down --rmi all
```

### 테스트 결과 초기화
```bash
rm -rf allure-results allure-report reports
```

---

## 🔧 문제 해결

### 포트 충돌 (3000번 포트 사용 중)
```bash
# 사용 중인 프로세스 확인
lsof -i :3000

# 프로세스 종료
kill -9 $(lsof -t -i:3000)
```

### Docker 이미지 빌드 오류
```bash
# 캐시 없이 재빌드
docker-compose build --no-cache
```

### 권한 문제 (Linux)
```bash
# Docker 그룹에 사용자 추가
sudo usermod -aG docker $USER
# 로그아웃 후 다시 로그인
```

---

## 🎨 Docker 이미지 특징

- **Base Image**: Python 3.12-slim
- **포함된 기능**:
  - ✅ 모든 Python 패키지 (pytest, requests, playwright 등)
  - ✅ Node.js & npm (Mock 서버용)
  - ✅ Playwright 브라우저 (Chromium, Firefox, WebKit)
  - ✅ Allure Report 생성 도구
  - ✅ 자동 헬스체크

---

## 💡 팁

1. **백그라운드 실행**
```bash
docker-compose up -d qa-test
docker-compose logs -f qa-test  # 로그 확인
```

2. **특정 테스트 파일 실행**
```bash
docker-compose run --rm qa-test pytest tests/api/test_registration_positive.py -v
```

3. **인터랙티브 모드**
```bash
docker-compose run --rm qa-test bash
# 컨테이너 내부에서 명령 실행
```

---

## 📝 요약

Docker를 사용하면:
- ✅ Python 버전 걱정 없음
- ✅ 의존성 충돌 없음
- ✅ 일관된 테스트 환경
- ✅ 한 명령으로 실행
- ✅ 어떤 OS에서도 동작

**가장 간단한 실행 방법:**
```bash
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project
docker-compose up qa-test
```

---

문제가 있으신가요? [GitHub Issues](https://github.com/jameshin1212/qa-automation-project/issues)에 문의해주세요!