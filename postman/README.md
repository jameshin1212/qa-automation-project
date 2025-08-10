# Postman Collection 사용 가이드

## 📦 파일 구성

- `WhaTap_QA_API_Tests.postman_collection.json` - API 테스트 컬렉션
- `WhaTap_QA_API.postman_environment.json` - 환경 변수 설정

## 🚀 Postman에서 Import 하기

### 1. Collection Import
1. Postman 앱 실행
2. 좌측 상단의 **Import** 버튼 클릭
3. `WhaTap_QA_API_Tests.postman_collection.json` 파일 선택
4. **Import** 클릭

### 2. Environment Import
1. 좌측 상단의 **Import** 버튼 클릭
2. `WhaTap_QA_API.postman_environment.json` 파일 선택
3. **Import** 클릭
4. 우측 상단의 Environment 드롭다운에서 **WhaTap QA API Environment** 선택

## 📋 테스트 구조

### 폴더 구성
```
WhaTap QA API Tests/
├── Positive Tests/          # 정상 케이스 (TC-001 ~ TC-004)
├── Negative Tests/          # 실패 케이스 (TC-005 ~ TC-012)
├── Boundary Tests/          # 경계값 테스트 (TC-013 ~ TC-017)
├── Security Tests/          # 보안 테스트 (TC-018 ~ TC-023)
├── Duplicate Tests/         # 중복 검사 (TC-024 ~ TC-025)
└── Cleanup/                 # 데이터 정리 유틸리티
```

## 🔧 사전 준비

### Mock Server 실행
```bash
cd mock_server
npm start
```

서버가 `http://localhost:3000`에서 실행되는지 확인

## ▶️ 테스트 실행 방법

### 개별 테스트 실행
1. Collections 탭에서 원하는 테스트 선택
2. **Send** 버튼 클릭
3. Response와 Test Results 확인

### 폴더별 실행
1. 폴더 우클릭 → **Run folder**
2. Collection Runner 창에서 설정 확인
3. **Run WhaTap QA API Tests** 클릭

### 전체 Collection 실행
1. Collection 이름 우클릭 → **Run collection**
2. 모든 테스트가 선택되었는지 확인
3. **Run WhaTap QA API Tests** 클릭

## ✅ 테스트 검증 항목

### Positive Tests
- HTTP 200 상태 코드
- 응답에 email, id 포함
- 패스워드 해싱 확인

### Negative Tests  
- HTTP 400 상태 코드
- 적절한 에러 코드 (INVALID_EMAIL, INVALID_PASSWORD, WEAK_PASSWORD)
- 에러 메시지 확인

### Boundary Tests
- 최소/최대 길이 처리
- 공백 제거 (trim) 동작
- 긴 입력값 처리

### Security Tests
- SQL Injection 차단
- XSS 공격 차단
- Path Traversal 차단
- 패스워드 암호화

### Duplicate Tests
- 중복 이메일 차단
- 대소문자 구분 없는 중복 검사

## 📊 테스트 결과 확인

### Test Results 탭
- 각 테스트의 Pass/Fail 상태
- 실패한 assertion 상세 정보

### Console
- 상세한 로그 정보
- 변수 값 확인
- 디버깅 정보

## 🔄 데이터 초기화

중복 테스트 실패 시 데이터 초기화:

1. **Cleanup** 폴더의 **Get All Users** 실행
2. 응답에서 user ID 확인
3. Environment 변수의 `userId`에 값 설정
4. **Delete User by ID** 실행

또는 Mock Server 재시작:
```bash
# DB 초기화
cp db-backup.json db.json
# 서버 재시작
npm start
```

## 🎯 주요 테스트 케이스

| TC ID | 테스트 명 | 예상 결과 |
|-------|----------|----------|
| TC-001 | 정상 등록 | 200 OK |
| TC-005 | @ 없는 이메일 | 400 Bad Request |
| TC-008 | 짧은 패스워드 | 400 Bad Request |
| TC-013 | 최소 길이 이메일 | 200 OK |
| TC-018 | SQL Injection | 400 Bad Request |
| TC-023 | 패스워드 암호화 | 200 OK + 해시된 패스워드 |
| TC-024 | 중복 이메일 | 400 Bad Request |

## 📝 참고사항

- 모든 테스트는 독립적으로 실행 가능
- 환경 변수를 통해 baseUrl 변경 가능
- Pre-request Scripts로 동적 데이터 생성
- Tests 스크립트로 자동 검증

## 🐛 문제 해결

### "Connection refused" 에러
→ Mock Server가 실행 중인지 확인

### 중복 테스트 실패
→ DB 초기화 후 재시도

### 테스트 순서 의존성
→ Collection Runner의 "Run collection" 사용하여 순차 실행