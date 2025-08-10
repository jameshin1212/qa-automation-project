# 🐳 Docker 실행 가이드

## 📋 사전 요구사항

- **Docker**: 20.10 이상
- **Docker Compose**: 2.0 이상

### Docker 설치
- **Mac/Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

## 🚀 빠른 시작 (Quick Start)

### 방법 1: 자동 스크립트 사용 (추천) 🎯
```bash
# 실행 권한 부여 (최초 1회)
chmod +x docker-run.sh

# 스크립트 실행
./docker-run.sh
```

### 방법 2: Docker Compose 직접 사용
```bash
# 전체 테스트 실행
docker-compose up

# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 방법 3: 단일 Docker 컨테이너 사용
```bash
# Docker 이미지 빌드
docker build -t whatap-qa-test .

# 컨테이너 실행
docker run -it --rm -p 3000:3000 whatap-qa-test
```

## 📦 Docker 구성

### 컨테이너 구조
```
whatap-qa-automation/
├── mock-server         # Mock API 서버 (포트: 3000)
├── test-runner        # 테스트 실행 환경
└── allure-ui          # Allure Report 서버 (포트: 5050) [선택사항]
```

### 포트 매핑
- **3000**: Mock API Server
- **5050**: Allure Report UI (선택사항)

## 🧪 테스트 실행 옵션

### 1. API 테스트만
```bash
docker-compose run --rm test-runner pytest tests/api -v
```

### 2. UI 테스트만
```bash
docker-compose run --rm test-runner pytest tests/ui -v
```

### 3. 전체 테스트
```bash
docker-compose run --rm test-runner pytest -v
```

### 4. Allure Report 생성
```bash
# 테스트 실행 후 리포트 생성
docker-compose run --rm test-runner bash -c "
  pytest --alluredir=allure-results -v &&
  allure generate allure-results -o allure-report --clean
"
```

### 5. Allure Report 서버 실행
```bash
# 프로필과 함께 실행
docker-compose --profile with-report up

# 브라우저에서 확인
open http://localhost:5050
```

## 🛠️ 유용한 명령어

### 컨테이너 관리
```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 컨테이너 중지
docker-compose stop

# 컨테이너 및 볼륨 삭제
docker-compose down -v

# 로그 확인
docker-compose logs mock-server
docker-compose logs test-runner
```

### 이미지 관리
```bash
# 이미지 재빌드
docker-compose build --no-cache

# 특정 서비스만 재빌드
docker-compose build mock-server
```

### 디버깅
```bash
# 컨테이너 내부 접속
docker-compose exec test-runner bash
docker-compose exec mock-server sh

# Mock Server 상태 확인
curl http://localhost:3000/config
```

## 📊 테스트 결과 확인

### 1. 콘솔 출력
테스트 실행 시 콘솔에 결과가 표시됩니다.

### 2. Allure Report
```bash
# HTML 리포트 생성
docker-compose run --rm test-runner allure generate allure-results -o allure-report

# 로컬에서 열기
open allure-report/index.html
```

### 3. 볼륨 마운트된 결과
- `./allure-results/`: 테스트 실행 결과
- `./allure-report/`: HTML 리포트
- `./reports/`: 기타 리포트

## ⚙️ 환경 변수 설정

### docker-compose.yml에서 수정
```yaml
environment:
  - API_BASE_URL=http://mock-server:3000
  - TEST_TIMEOUT=60
  - BROWSER=chromium
```

### .env 파일 사용
```bash
# .env 파일 생성
echo "API_BASE_URL=http://mock-server:3000" > .env
echo "TEST_BROWSER=webkit" >> .env
```

## 🔧 문제 해결

### 1. 포트 충돌
```bash
# 3000 포트 사용 중인 프로세스 확인
lsof -i :3000

# docker-compose.yml에서 포트 변경
ports:
  - "3001:3000"  # 3001로 변경
```

### 2. 권한 문제
```bash
# 볼륨 권한 문제 해결
sudo chown -R $(whoami):$(whoami) allure-results allure-report
```

### 3. 메모리 부족
Docker Desktop 설정에서 메모리 할당 증가:
- Mac/Windows: Docker Desktop → Preferences → Resources
- 권장: 최소 4GB RAM

### 4. 네트워크 문제
```bash
# Docker 네트워크 재생성
docker-compose down
docker network prune -f
docker-compose up
```

## 🎯 CI/CD 통합

### GitHub Actions
```yaml
- name: Run tests in Docker
  run: |
    docker-compose up -d mock-server
    docker-compose run --rm test-runner
    docker-compose down
```

### Jenkins
```groovy
stage('Test') {
    steps {
        sh 'docker-compose up --abort-on-container-exit'
    }
}
```

## 📝 채용 담당자를 위한 체크리스트

✅ **필수 확인 사항:**
1. Docker Desktop 설치 여부
2. 포트 3000, 5050 사용 가능 여부
3. 최소 4GB RAM 할당

✅ **간단 실행 순서:**
```bash
# 1. 프로젝트 클론
git clone [repository-url]
cd qa-automation-project

# 2. Docker로 테스트 실행
./docker-run.sh

# 3. 옵션 2 선택 (전체 테스트)
# 4. 테스트 결과 확인
```

✅ **예상 소요 시간:**
- Docker 이미지 빌드: 3-5분 (최초)
- API 테스트: 15초
- UI 테스트: 10초
- 전체 테스트: 30초

## 💡 팁

1. **빠른 실행**: `./docker-run.sh` 사용 권장
2. **리포트 확인**: Allure Report로 상세 결과 확인
3. **로그 확인**: `docker-compose logs -f` 로 실시간 로그 확인
4. **정리**: 테스트 후 `docker-compose down -v` 로 정리

---

문의사항이 있으시면 README.md의 연락처로 문의 부탁드립니다.