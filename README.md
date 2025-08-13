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
│   └── test_cases.xlsx          # Excel 테스트 케이스 명세서
├── reports/                      # 테스트 실행 결과
│   ├── QA_api_ui_automation_report.pdf  # 전체 테스트 결과 PDF (31개 테스트 100% 통과)
│   └── README.md                # 리포트 설명 문서
├── .github/workflows/            # GitHub Actions CI/CD
│   └── test-automation.yml      # 자동화된 테스트 파이프라인
├── postman/                     # Postman 테스트
│   ├── WhaTap_QA_API.postman_environment.json  # Postman 환경 변수
│   ├── WhaTap_QA_API_Tests.postman_collection.json  # API 테스트 컬렉션
│   └── README.md                # Postman 테스트 가이드
├── allure-results/              # Allure 리포트 원시 데이터
├── conftest.py                  # 전역 pytest 설정 및 픽스처
├── pytest.ini                   # pytest 실행 설정 파일
├── requirements.txt             # Python 패키지 의존성 목록
├── docker-compose.yml           # Docker Compose 설정
├── Dockerfile                   # Docker 이미지 빌드 설정
├── docker_test.sh              # Docker 컨테이너 테스트 스크립트
├── run_tests.sh                # 로컬 테스트 실행 스크립트
├── run_ui_tests_local.sh       # UI 테스트 로컬 실행 스크립트
├── run_with_allure.sh          # Allure 리포트 포함 테스트 실행
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

```bash
# 1. Docker로 실행
docker-compose up -d qa-server

# 2. 로컬에서 UI 테스트 실행
npm install --prefix mock_server
pytest tests/ui/ --headed --slowmo=1000
```

## 🔄 CI/CD 실행 방법 (GitHub Actions)

### 📋 자동 실행 (Push/PR 시)

GitHub Actions는 다음 이벤트 발생 시 자동으로 실행됩니다:

- **Push**: `main` 또는 `develop` 브랜치에 코드 Push 시
- **Pull Request**: `main` 브랜치로 PR 생성 시

### 🎯 수동 실행 (Workflow Dispatch)

GitHub 리포지토리에서 직접 워크플로우를 실행할 수 있습니다:

1. **GitHub 리포지토리 접속**
   - https://github.com/[your-username]/qa-automation-project

2. **Actions 탭 클릭**
   - 상단 메뉴에서 `Actions` 탭 선택

3. **워크플로우 선택**
   - 왼쪽 사이드바에서 `QA Automation Tests` 워크플로우 선택

4. **Run workflow 클릭**
   - 오른쪽 상단의 `Run workflow` 버튼 클릭
   - 테스트 타입 선택:
     - `all`: 모든 테스트 실행 (기본값)
     - `api`: API 테스트만 실행
     - `ui`: UI 테스트만 실행
     - `smoke`: Smoke 테스트만 실행

5. **실행 및 결과 확인**
   - `Run workflow` 버튼 클릭하여 실행
   - 실행 중인 워크플로우 클릭하여 실시간 로그 확인
   - 완료 후 `Artifacts` 섹션에서 테스트 결과 다운로드 가능

### 📊 테스트 결과 확인

CI/CD 실행 후 결과를 확인하는 방법:

1. **실행 요약 (Summary)**
   - 각 워크플로우 실행 페이지 하단에 테스트 요약 표시
   - API/UI 테스트 완료 상태 확인

2. **아티팩트 다운로드 (Artifacts)**
   - `test-results` 아티팩트 다운로드
   - 포함 내용:
     - `reports/`: HTML 테스트 리포트
     - `allure-report/`: Allure 대화형 리포트

3. **실패 시 디버깅**
   - 워크플로우 로그에서 실패한 테스트 상세 정보 확인
   - Mock Server 시작 실패 시 서버 로그 확인
   - Playwright 브라우저 설치 오류 시 의존성 확인

### ⚙️ GitHub Actions 워크플로우 구성

워크플로우 파일: `.github/workflows/test-automation.yml`

### 🔧 CI/CD 문제 해결

**일반적인 문제와 해결 방법:**

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| Mock Server 시작 실패 | 포트 충돌 또는 db.json 누락 | db-backup.json 자동 생성 로직 확인 |
| Playwright 설치 실패 | Ubuntu 패키지 의존성 | 워크플로우에 수동 의존성 설치 포함됨 |
| 테스트 타임아웃 | Mock Server 응답 지연 | 서버 준비 대기 시간 증가 |
| 아티팩트 업로드 실패 | 권한 문제 | GitHub 리포지토리 Actions 권한 확인 |

## 🐛 교육 목적 버그 (QA 시연용)

### 의도적으로 주입된 버그들

이 프로젝트는 QA의 가치를 시연하기 위해 **의도적으로 4개의 버그를 포함**하고 있습니다:

| 버그 ID | 설명 | 심각도 | 영향 |
|---------|------|--------|------|
| BUG-TC-008 | 7자 비밀번호 허용 | HIGH | 보안 정책 위반 |
| BUG-TC-010 | 소문자 없는 비밀번호 허용 | HIGH | 약한 비밀번호 |
| BUG-TC-020 | 특정 XSS 패턴 미차단 | CRITICAL | 보안 취약점 |
| BUG-TC-024 | 중복 이메일 허용 | HIGH | 데이터 무결성 |

### 버그 활성화/비활성화

버그는 환경 변수로 제어 가능합니다:

```bash
# 모든 버그 비활성화
export BUG_SHORT_PASSWORD=false
export BUG_NO_LOWERCASE=false
export BUG_XSS_BYPASS=false
export BUG_DUPLICATE_ALLOW=false

# Mock Server 재시작
npm start --prefix mock_server
```

### 버그 감지 테스트 실행

```bash
# 버그 감지 테스트만 실행
pytest tests/api/test_bug_detection.py -v

# 테스트 리포트 생성
python generate_test_report.py
```

### 교육적 목적

1. **QA의 가치 입증**: 버그를 발견하고 리포팅하는 능력
2. **현실적 시나리오**: 실제 개발에서 자주 발생하는 버그 유형
3. **개선 제안**: 각 버그에 대한 구체적인 해결책 제시
4. **품질 메트릭**: 테스트 커버리지와 버그 발견율 측정





      
 


## 📊 테스트 실행 결과 요약

**실행 일시**: 2025-08-14 01:15:00  
**테스트 환경**: Local Development (Mock Server with Educational Bugs)

### 전체 결과
- **총 테스트**: 31건 (API: 25건, UI: 6건)
- **성공**: 27건 (87.1%)
- **실패**: 4건 (12.9%)
- **상태**: ⚠️ **주요 이슈 발견 - 즉시 조치 필요**

### 🐛 발견된 이슈 (4건)

#### 1. 🟠 [HIGH] 비밀번호 최소 길이 검증 실패
- **테스트 ID**: BUG-TC-008
- **증상**: 7자 비밀번호가 허용됨 (최소 8자 요구사항 위반)
- **재현**: `password="Test12!"` (7자) → 200 OK (예상: 400 Error)
- **영향**: 보안 정책 위반, 브루트포스 공격 취약성 증가
- **권장 조치**: middleware.js 51-56라인 검증 로직 수정

#### 2. 🟠 [HIGH] 비밀번호 복잡도 검증 우회
- **테스트 ID**: BUG-TC-010  
- **증상**: 소문자 없는 비밀번호 "NOLOWERCASE123!" 허용
- **영향**: 약한 비밀번호 허용으로 계정 탈취 위험 증가
- **권장 조치**: middleware.js 73-77라인 복잡도 검증 수정

#### 3. 🔴 [CRITICAL] XSS 방어 우회 취약점
- **테스트 ID**: BUG-TC-020
- **증상**: `<script>alert('XSS')</script>@test.com` 패턴 미차단
- **영향**: Cross-Site Scripting 공격 가능
- **권장 조치**: 즉시 XSS 필터링 강화, CSP 헤더 구현

#### 4. 🟠 [HIGH] 중복 이메일 등록 허용
- **테스트 ID**: BUG-TC-024
- **증상**: 동일 이메일로 여러 계정 생성 가능
- **영향**: 데이터 무결성 위반
- **권장 조치**: middleware.js 94-105라인 중복 체크 수정

### 📈 테스트 카테고리별 결과

| 카테고리 | 테스트 수 | 성공 | 실패 | 성공률 | 비고 |
|---------|-----------|------|------|--------|------|
| Positive Tests | 4 | 4 | 0 | 100% | ✅ 정상 |
| Negative Tests | 8 | 6 | 2 | 75% | ⚠️ 검증 실패 |
| Boundary Tests | 5 | 5 | 0 | 100% | ✅ 정상 |
| Security Tests | 6 | 5 | 1 | 83.3% | 🔴 XSS 취약 |
| Duplicate Tests | 2 | 1 | 1 | 50% | ⚠️ 중복 허용 |
| UI Tests | 6 | 6 | 0 | 100% | ✅ 정상 |
| **Bug Detection** | **4** | **0** | **4** | **0%** | **🐛 버그 발견** |
| **총계** | **31** | **27** | **4** | **87.1%** | **⚠️ 조치 필요** |

### 🎯 우선순위별 조치 계획

#### 🔴 긴급 (24시간 내)
1. **XSS 취약점 패치** - 가장 심각한 보안 위협
2. **비밀번호 검증 로직 수정** - 기본 보안 요구사항

#### 🟠 높음 (1주일 내)
1. **중복 이메일 체크 로직 수정**
2. **입력 검증 단위 테스트 추가**
3. **보안 헤더 구현 (CSP, X-Frame-Options 등)**

#### 🟡 중간 (1개월 내)
1. **자동화된 보안 스캔 도입**
2. **비밀번호 정책 문서화**
3. **에러 메시지 표준화**

#### 🟢 낮음 (분기 내)
1. **WAF 도입 검토**
2. **정적 코드 분석 도구 통합**
3. **침투 테스트 수행**

### 📋 테스트 실행 증거

```bash
# 버그 감지 테스트 실행
$ pytest tests/api/test_bug_detection.py -v

FAILED test_bug_short_password - 7자 비밀번호 허용됨
FAILED test_bug_no_lowercase - 소문자 없는 비밀번호 허용됨
FAILED test_bug_xss_bypass - XSS 패턴 차단 실패
FAILED test_bug_duplicate_email - 중복 이메일 허용됨

실패율: 12.9% (4/31 테스트 실패)
```

### 📝 참고 사항
- 이 리포트는 QA 채용과제 제출용으로, 교육 목적의 의도적 버그를 포함합니다
- 실제 프로덕션 환경에서는 이러한 버그가 배포 전에 반드시 수정되어야 합니다
- 버그는 환경 변수 `BUG_*=false`로 비활성화 가능합니다
- 자세한 버그 정보는 `/tests/api/test_bug_detection.py` 참조
