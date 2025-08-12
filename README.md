# 🧪 QA Automation Project - User Registration System

## 📌 프로젝트 소개
안녕하세요.
QA지원자 신동혁 입니다. 해당 프로젝트는 웹 애플리케이션의 **사용자 등록 시스템**에 대한 종합적인 품질 검증을 위한 자동화 테스트 프레임워크입니다. API와 UI 레벨에서 체계적인 테스트를 수행하고, CI/CD 파이프라인과 통합되어 지속적인 품질 모니터링을 제공합니다.

### 🎯 주요 특징
- ✅ **31개 테스트 케이스** (API: 25개, UI: 6개)
- 🤖 **100% 자동화 구현**
- 📊 **Allure Report 통합**
- 🔄 **GitHub Actions CI/CD**

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

## 💼 Pre-Condition

### ⚠️ Python 버전 호환성
- **권장**: Python 3.12

1. **프로젝트 클론**
```bash
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project
```

2. **Python 가상환경 설정**
```bash
# Python 3.12 권장 (모든 기능 지원)
  python3.12 -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Python 의존성 설치**
```bash
# 전체 패키지 설치 (Python 3.8-3.12)
pip install -r requirements.txt
```

4. **Playwright 브라우저 설치**
```bash
playwright install webkit
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

### 2️⃣ 테스트 실행
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

**Smoke 테스트:** ##
```bash
pytest -m smoke -v # 핵심 기능 테스트
```

**특정 카테고리:**
```bash
pytest -m security -v  # 보안 테스트
pytest -m boundary -v  # 경계값 테스트
pytest -m negative -v  # 네거티브 테스트
```

### 5️⃣ Allure Report 생성

#### 수동 실행
```bash
# Allure 데이터 생성하면서 테스트 실행
pytest tests/api -v --alluredir=allure-results

# 브라우저에서 리포트 보기
allure serve allure-results

# 또는 HTML 파일로 생성
allure generate allure-results -o allure-report --clean
open allure-report/index.html
```


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

🖥️ 프로젝트 클론
### 1. **git**
```bash
git clone https://github.com/jameshin1212/qa-automation-project
cd qa-automation-project
```
🐳 Docker 테스트 실행 순서

### 0. 🐳Docker 백그라운드 실행(mock server실행)
```bash
docker-compose up -d mock-server 
#```docker-compose down```(docker종료)
```
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
### 4. 리포트 확인
```bash
allure serve allure-results
```
### 5. 리포트 초기화
```bash
# 자동 스크립트 사용 (추천)
./clean-reports.sh
# 또는 수동 초기화
rm -rf allure-results allure-report reports .pytest_cache
mkdir -p allure-results allure-report reports
```
### 6. 데이터 초기화
```bash
# 자동 스크립트 사용
 ./reset-db.sh
 ```









🤖 브라우저 GUI 자동화 테스트 실행 (로컬)

### 0. Python 가상환경 설정
```bash
python3 -m venv venv
source venv/bin/activate 
#```deactivate```(가상환경 종료)
```
### 1. mock_server 실행 (새로운 터미널 창)
```bash
cd mock_server
npm start
#```  kill -9 $(lsof -t -i:3000)```(mock_server종료)
```
### 2. 브라우저 GUI 테스트 
```bash
# 브라우저 화면 표시 모드 (테스트 동작 확인)
pytest tests/ui -v --headed
# 느린 모션으로 동작 관찰
pytest tests/ui -v --headed --slowmo=2000
``` 




      
 