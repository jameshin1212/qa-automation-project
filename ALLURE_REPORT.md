# 📊 Allure Report 실행 가이드

## 🚀 빠른 시작 (3단계)

```bash
# 1. 테스트 실행 (Allure 결과 생성)
docker-compose run --rm all-test

# 2. Allure Report 생성
docker-compose run allure-generate

# 3. Report 서버 시작
docker-compose up -d allure-serve
```

브라우저에서 **http://localhost:9090** 접속

---

## 📝 상세 설명

### 1️⃣ 테스트 실행
먼저 테스트를 실행하여 `allure-results` 디렉토리에 결과를 생성합니다:

```bash
# 전체 테스트
docker-compose run --rm all-test

# 또는 개별 테스트
docker-compose run --rm api-test
docker-compose run --rm ui-test
```

### 2️⃣ Report 생성
테스트 결과를 기반으로 HTML 리포트를 생성합니다:

```bash
docker-compose run allure-generate
```

이 명령은 `allure-report` 디렉토리에 정적 HTML 파일들을 생성합니다.

### 3️⃣ Report 확인
생성된 리포트를 웹 서버로 제공합니다:

```bash
docker-compose up -d allure-serve
```

브라우저에서 **http://localhost:9090** 접속하여 리포트를 확인합니다.

---

## 🔧 대체 방법

### Python HTTP 서버 사용
Docker 없이 간단히 리포트를 확인하려면:

```bash
# Report 생성 후
cd allure-report
python3 -m http.server 8888
```

브라우저에서 **http://localhost:8888** 접속

### 스크립트 사용
```bash
./allure_simple.sh
```

---

## 🎯 한 번에 실행

```bash
# 모든 단계를 한 번에 실행
docker-compose run --rm all-test && \
docker-compose run allure-generate && \
docker-compose up -d allure-serve && \
echo "✅ Allure Report: http://localhost:9090"
```

---

## 📌 주의사항

- 테스트를 먼저 실행해야 리포트 생성이 가능합니다
- 포트 충돌 시 `docker-compose.yml`에서 포트 변경 가능
- `allure-results` 디렉토리가 비어있으면 리포트 생성 실패

---

## 🧹 정리

```bash
# 서비스 중지
docker-compose down

# 결과 파일 삭제
rm -rf allure-results allure-report
```