# 🧪 QA Automation Project - User Registration System

## 📌 프로젝트 소개
안녕하세요.
QA지원자 신동혁 입니다. 해당 프로젝트는 웹 애플리케이션의 **사용자 등록 시스템**에 대한 종합적인 품질 검증을 위한 자동화 테스트 프레임워크입니다. API와 UI 레벨에서 체계적인 테스트를 수행하고, CI/CD 파이프라인과 통합되어 지속적인 품질 모니터링을 제공합니다.

### 🎯 주요 특징
- ✅ **31개 테스트 케이스** (API: 25개, UI: 6개)
- 🤖 **100% 자동화 구현**
- 📊 **Allure Report 통합**
- 🔄 **GitHub Actions CI/CD**
- 📝 **체계적인 테스트 문서화**

## 🏗️ 기술 스택

| 영역 | 기술 | 설명 |
|------|------|------|
| **API Testing** | pytest + requests | Python 기반 API 테스트 프레임워크 |
| **UI Testing** | Playwright | 크로스 브라우저 E2E 테스트 자동화 |
| **Mock Server** | JSON Server | RESTful API Mock 서버 |
| **Reporting** | Allure Report | 대화형 테스트 결과 리포트 |
| **CI/CD** | GitHub Actions | 자동화된 테스트 실행 파이프라인 |
| **Documentation** | Excel + Markdown | 테스트 케이스 및 실행 가이드 |

## 📁 프로젝트 구조

```
qa-automation-project/
├── mock_server/                    # JSON Server Mock API 서버
│   ├── db.json                    # 테스트 데이터베이스 (사용자, 설정)
│   ├── db-backup.json             # 초기 상태 백업 파일
│   ├── public/                    # 정적 웹 파일
│   │   └── index.html            # 사용자 등록 웹 페이지 (테스트용 UI)
│   ├── package.json              # Node.js 프로젝트 설정 및 의존성
│   └── package-lock.json         # 정확한 의존성 버전 잠금
├── tests/                         # 테스트 코드 루트
│   ├── api/                      # REST API 테스트
│   │   ├── base_api_test.py      # API 테스트 기본 클래스 (공통 메서드)
│   │   ├── test_registration_positive.py    # 정상 플로우 테스트 (4개)
│   │   ├── test_registration_negative.py    # 비정상 플로우 테스트 (8개)
│   │   ├── test_registration_boundary.py    # 경계값 테스트 (5개)
│   │   ├── test_registration_security.py    # 보안 테스트 (6개)
│   │   └── test_registration_duplicate.py   # 중복 방지 테스트 (2개)
│   ├── ui/                       # 웹 UI 테스트
│   │   ├── pages/                # Page Object Model 패턴
│   │   │   └── registration_page.py  # 회원가입 페이지 객체
│   │   ├── conftest.py           # UI 테스트 설정 및 픽스처
│   │   └── test_registration_ui.py   # UI 자동화 테스트 (6개)
│   └── fixtures/                 # 테스트 데이터
│       └── test_data.json        # 테스트 케이스별 입력 데이터
├── docs/                         # 문서화
│   ├── test_cases.xlsx          # Excel 테스트 케이스 명세서
│   ├── generate_test_cases.py   # Excel 문서 생성 스크립트
│   └── generate_test_cases_simple.py  # 간소화된 Excel 생성기
├── reports/                      # 테스트 실행 결과
│   └── debug_db_*.json          # 실패한 테스트의 DB 상태 스냅샷
├── .github/workflows/            # GitHub Actions CI/CD
│   └── test-automation.yml      # 자동화된 테스트 파이프라인
├── allure-results/              # Allure 리포트 원시 데이터
├── venv/                        # Python 가상환경
├── conftest.py                  # 전역 pytest 설정 및 픽스처
├── pytest.ini                  # pytest 실행 설정 파일
├── requirements.txt             # Python 패키지 의존성 목록
├── requirements-minimal.txt     # 최소 의존성 (호환성 문제 해결용)
├── run_tests.sh                # 테스트 실행 배치 스크립트
└── README.md                   # 프로젝트 가이드 문서
```

## 🚀 빠른 시작

### 📋 사전 요구사항
- Python 3.8 이상
- Node.js 16 이상
- Git

### 🔧 설치 방법

1. **프로젝트 클론**
```bash
git clone <repository-url>
cd qa-automation-project
```

2. **Python 가상환경 설정**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Python 의존성 설치**
```bash
pip install -r requirements.txt
```

4. **Playwright 브라우저 설치**
```bash
# macOS에서 권장: webkit 브라우저 사용
playwright install webkit

# 또는 다른 브라우저 (chromium은 macOS에서 불안정할 수 있음)
playwright install firefox
```

5. **Mock 서버 설치**
```bash
cd mock_server
npm install
cd ..
```

## 🏃‍♂️ 테스트 실행

### 1️⃣ Mock 서버 시작
```bash
cd mock_server
npm start
# 서버가 http://localhost:3000 에서 실행됩니다
```

### 2️⃣ 전체 테스트 실행
새 터미널에서:
```bash
pytest -v
```

### 3️⃣ 특정 테스트 실행

**API 테스트만:**
```bash
pytest tests/api -v
```

**UI 테스트만:**
```bash
# 기본 (headless 모드)
pytest tests/ui -v

# 브라우저 화면 표시 모드 (테스트 동작 확인)
pytest tests/ui -v --headed

# 느린 모션으로 동작 관찰
pytest tests/ui -v --headed --slowmo=2000
```

**Smoke 테스트:**
```bash
pytest -m smoke -v
```

**특정 카테고리:**
```bash
pytest -m security -v  # 보안 테스트
pytest -m boundary -v  # 경계값 테스트
pytest -m negative -v  # 네거티브 테스트
```

### 4️⃣ 브라우저 설정

**UI 테스트 브라우저 옵션:**
```bash
# webkit (macOS 권장)
pytest tests/ui --browser=webkit --headed

# firefox (안정적인 대안)
pytest tests/ui --browser=firefox --headed

# chromium (일부 macOS에서 불안정)
pytest tests/ui --browser=chromium --headed
```

**주요 플래그:**
- `--headed`: 브라우저 화면 표시 (기본은 headless)
- `--slowmo=2000`: 액션 간 2초 지연 (동작 관찰용)
- `--browser=webkit`: 브라우저 엔진 지정

### 5️⃣ Allure Report 생성
```bash
# 테스트 실행 with Allure
pytest --alluredir=allure-results

# 리포트 생성 및 열기
allure serve allure-results
```

## 📊 테스트 케이스 요약

### 카테고리별 분포
| 카테고리 | API | UI | 합계 | 우선순위 |
|---------|-----|-----|------|----------|
| **정상 플로우** | 4 | 1 | 5 | Critical |
| **비정상 플로우** | 8 | 3 | 11 | High |
| **경계값** | 5 | 0 | 5 | Medium |
| **보안** | 6 | 0 | 6 | Critical |
| **중복 방지** | 2 | 1 | 3 | High |
| **UI 검증** | 0 | 1 | 1 | Medium |
| **총계** | **25** | **6** | **31** | - |

### 주요 검증 항목
- ✅ 이메일 형식 검증
- ✅ 비밀번호 복잡도 (최소 8자, 대소문자, 숫자, 특수문자)
- ✅ 필수 필드 검증
- ✅ 중복 이메일 방지
- ✅ SQL Injection 방어
- ✅ XSS 공격 방어
- ✅ 비밀번호 암호화

## 🔄 CI/CD 파이프라인

GitHub Actions를 통한 자동화된 테스트 실행:

1. **트리거 조건**
   - `main`, `develop` 브랜치 푸시
   - Pull Request 생성
   - 수동 실행 (workflow_dispatch)

2. **실행 단계**
   - 환경 설정 (Python, Node.js)
   - 의존성 설치
   - Mock 서버 시작
   - 테스트 실행
   - Allure Report 생성
   - 결과 아티팩트 업로드

3. **테스트 결과**
   - GitHub Pages에 Allure Report 자동 배포
   - PR에 테스트 요약 코멘트


## 🐛 문제 해결

### Mock 서버 연결 실패
```bash
# 포트 확인
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# 프로세스 종료 후 재시작
kill -9 <PID>
cd mock_server && npm start
```

### Playwright 브라우저 오류
```bash
# 브라우저 재설치
playwright install --force chromium
playwright install-deps
```

### 테스트 실패 디버깅
```bash
# 상세 로그와 함께 실행
pytest -vv --log-cli-level=DEBUG

# 특정 테스트만 실행
pytest tests/api/test_registration_positive.py::TestRegistrationPositive::test_registration_valid_email_password_success -v
```
