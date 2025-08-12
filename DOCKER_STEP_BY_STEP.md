# 🐳 Docker 단계별 실행 가이드

채용 담당자님을 위한 **명확한 단계별 실행 가이드**입니다.

---

## 📋 Step 1: Docker 설정 및 빌드

```bash
# 1-1. 프로젝트 클론
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project

# 1-2. Docker 이미지 빌드 (약 2-3분 소요)
docker-compose build

# ✅ 성공 확인: "Successfully built" 메시지 출력
```

---

## 🚀 Step 2: Mock 서버 시작

```bash
# 2-1. Mock 서버 백그라운드 실행
docker-compose up -d qa-server

# 2-2. 서버 상태 확인 (약 10초 대기 후)
docker-compose ps

# ✅ 성공 확인:
# NAME               STATUS
# whatap-qa-server   Up (healthy)

# 2-3. Mock 서버 동작 확인
curl http://localhost:3000/config

# ✅ 성공 확인: JSON 설정 데이터 출력
```

---

## 🧪 Step 3: API 테스트 실행

```bash
# 3-1. API 테스트 실행 (25개 테스트 케이스)
docker-compose run --rm api-test

# ⏱️ 소요 시간: 약 10-15초

# ✅ 성공 확인:
# ================================
# collected 25 items
# tests/api/test_registration_positive.py ....
# tests/api/test_registration_negative.py ........
# tests/api/test_registration_boundary.py .....
# tests/api/test_registration_security.py ......
# tests/api/test_registration_duplicate.py ..
# ================================
# ✅ API Tests Completed!
# Total: 25 API test cases executed
```

### API 테스트 구성:
- ✅ **Positive Tests** (4개): 정상 시나리오
- ✅ **Negative Tests** (8개): 오류 처리
- ✅ **Boundary Tests** (5개): 경계값 검증
- ✅ **Security Tests** (6개): 보안 취약점
- ✅ **Duplicate Tests** (2개): 중복 방지

---

## 🖥️ Step 4: UI 테스트 실행

```bash
# 4-1. UI 테스트 실행 (6개 테스트 케이스)
docker-compose run --rm ui-test

# ⏱️ 소요 시간: 약 10-20초

# ✅ 성공 확인:
# ================================
# collected 6 items
# tests/ui/test_registration_ui.py ......
# ================================
# ✅ UI Tests Completed!
# Total: 6 UI test cases executed
```

### UI 테스트 구성:
- ✅ **회원가입 플로우**: 전체 등록 과정
- ✅ **실시간 검증**: 입력 필드 검증
- ✅ **에러 처리**: 오류 메시지 표시
- ✅ **중복 검사**: 이메일 중복 확인

---

## 📊 Step 5: Allure Report 확인

```bash
# 5-1. Allure Report 서버 시작
docker-compose up -d allure-report

# 5-2. 브라우저에서 리포트 확인
# 🌐 http://localhost:5050 접속

# ✅ 성공 확인:
# - 전체 테스트 통계 차트
# - Pass/Fail 비율 (31/31 = 100%)
# - 각 테스트 상세 결과
# - 실행 시간 분석
```

### Allure Report 내용:
- 📈 **Overview**: 전체 성공률 및 통계
- 📋 **Suites**: 테스트 카테고리별 결과
- ⏱️ **Timeline**: 실행 시간 분석
- 📸 **Screenshots**: UI 테스트 스크린샷

---

## 🎯 선택사항: 전체 테스트 한번에 실행

```bash
# 모든 테스트 한번에 실행 (31개)
docker-compose run --rm all-test

# ✅ 성공 확인:
# Total: 31 test cases (25 API + 6 UI) executed
# ============================= 31 passed in 20s =============================
```

---

## 🛑 Step 6: 종료 및 정리

```bash
# 6-1. 모든 서비스 중지
docker-compose down

# 6-2. 테스트 결과 보관 (선택사항)
# allure-results/ 폴더에 테스트 결과 저장됨
# allure-report/ 폴더에 HTML 리포트 저장됨
```

---

## ✅ 전체 실행 요약

```bash
# 간단 5줄 명령어로 전체 테스트 실행
docker-compose build                    # 1. 빌드
docker-compose up -d qa-server          # 2. Mock 서버 시작
docker-compose run --rm api-test       # 3. API 테스트
docker-compose run --rm ui-test        # 4. UI 테스트
docker-compose up -d allure-report     # 5. 리포트 확인 (http://localhost:5050)
```

---

## 📈 예상 결과 요약

| 항목 | 개수 | 상태 | 소요시간 |
|------|------|------|----------|
| API 테스트 | 25개 | ✅ Pass | 10-15초 |
| UI 테스트 | 6개 | ✅ Pass | 10-20초 |
| **전체** | **31개** | **✅ 100% Pass** | **20-30초** |

---

## 🆘 문제 발생 시

### Q1: 포트 3000 또는 5050이 사용 중입니다
```bash
# Mac/Linux
kill -9 $(lsof -t -i:3000)
kill -9 $(lsof -t -i:5050)

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Q2: Docker 이미지 빌드가 실패합니다
```bash
# Docker 캐시 정리 후 재빌드
docker system prune -f
docker-compose build --no-cache
```

### Q3: 테스트가 실패합니다
```bash
# 상세 로그 확인
docker-compose logs qa-server
docker-compose run --rm api-test pytest tests/api -vvv
```

---

## 💡 핵심 포인트

1. **환경 독립성**: Python 버전, 의존성 문제 없음
2. **단계별 실행**: 각 단계를 명확히 구분하여 확인 가능
3. **시각적 리포트**: Allure를 통한 상세한 테스트 결과
4. **100% 자동화**: 수동 개입 없이 전체 프로세스 실행

---

**문의사항**: GitHub Issues 또는 README의 연락처로 문의 부탁드립니다.