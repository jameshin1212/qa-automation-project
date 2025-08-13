# 🧪 QA Automation Project - User Registration System

## 📌 프로젝트 소개
안녕하세요.
QA지원자 신동혁 입니다. 해당 프로젝트는 웹 애플리케이션의 **사용자 등록 시스템**에 대한 종합적인 품질 검증을 위한 자동화 테스트 프레임워크입니다. API와 UI 레벨에서 체계적인 테스트를 수행하고, CI/CD 파이프라인과 통합되어 지속적인 품질 모니터링을 제공합니다.

### 🎯 주요 특징
- ✅ **31개 테스트 케이스** (API: 25개, UI: 6개)
- 🤖 **100% 자동화 구현**
- 📊 **Allure Report 통합**
- 🔄 **GitHub Actions CI/CD**
- 🐳 **Docker 지원으로 환경 독립적 실행**

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
│   ├── QA_api_ui_automation_report.pdf  # 전체 테스트 결과 PDF (31개 테스트 100% 통과)
│   └── README.md                # 리포트 설명 문서
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
## 📝 실행 방법

### 🚀 Docker 환경에서 실행 (Headless Mode)

```bash
# 1. 프로젝트 클론
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project

# 2. Docker 빌드 및 서버 시작
docker-compose build
docker-compose up -d qa-server

# 3. 테스트 실행 (Headless 모드)
docker-compose run --rm all-test

# 4. Allure Report 생성 및 확인
docker-compose run allure-generate
docker-compose up -d allure-serve
# 브라우저에서 http://localhost:9090 접속
```

### 🖥️ 브라우저에서 UI 테스트 직접 확인하기 (Headed Mode)

UI 테스트가 실제 브라우저에서 어떻게 동작하는지 시각적으로 확인하려면:

> ⚠️ **중요**: Python 3.13은 일부 의존성과 호환성 문제가 있을 수 있습니다. Python 3.10~3.12 사용을 권장합니다.

```bash
# 1. Python 버전 확인 (3.10~3.12 권장)
python3 --version

# 2. Python 가상환경 설정
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 만약 greenlet 설치 오류가 발생하면:
# - Python 3.12 이하 버전 사용 권장
# - 또는 Docker 환경 사용 (위의 Docker 실행 방법 참조)

# 4. Playwright 브라우저 설치
playwright install chromium

# 5. Mock 서버 시작 (별도 터미널)
cd mock_server
npm install
npm start

# 6. UI 테스트를 브라우저 모드로 실행
pytest tests/ui/ --headed --slowmo=1000

# 옵션 설명:
# --headed: 실제 브라우저 창을 열어서 테스트 진행
# --slowmo=1000: 각 동작 사이에 1초 대기 (동작을 천천히 확인)
```

#### 🎯 개별 UI 테스트 실행 예시

```bash
# 특정 테스트만 브라우저에서 확인
pytest tests/ui/test_registration_ui.py::TestRegistrationUI::test_successful_registration --headed --slowmo=500

# 디버그 모드로 실행 (더 자세한 로그)
PWDEBUG=1 pytest tests/ui/ --headed
```

### 📋 테스트 모드 비교

| 모드 | 실행 방법 | 장점 | 용도 |
|------|----------|------|------|
| **Headless (Docker)** | `docker-compose run --rm ui-test` | 빠른 속도, CI/CD 적합, 환경 독립적 | 자동화 파이프라인 |
| **Headed (로컬)** | `pytest tests/ui/ --headed` | 시각적 확인 가능 | 디버깅, 데모 |
| **Debug (로컬)** | `PWDEBUG=1 pytest tests/ui/ --headed` | 단계별 실행 | 문제 해결 |

### 🔧 트러블슈팅

#### Python 버전 호환성 문제
만약 `greenlet` 설치 오류가 발생하면:

1. **Python 3.12 사용 (권장)**:
   ```bash
   # macOS (Homebrew)
   brew install python@3.12
   python3.12 -m venv venv
   
   # Ubuntu/Debian
   sudo apt install python3.12 python3.12-venv
   python3.12 -m venv venv
   ```

2. **Docker 환경 사용 (가장 안정적)**:
   ```bash
   docker-compose run --rm all-test
   ```

3. **requirements-minimal.txt 사용**:
   ```bash
   pip install -r requirements-minimal.txt
   ```




      
 