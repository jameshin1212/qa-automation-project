# 📊 테스트 결과 리포트

이 폴더는 QA 자동화 테스트의 실행 결과를 포함합니다.

## 📄 포함된 파일

### QA_api_ui_automation_report.pdf
- **내용**: API 및 UI 테스트 전체 결과
- **테스트 항목**:
  - API 테스트: 25개 (모두 통과 ✅)
  - UI 테스트: 6개 (모두 통과 ✅)
- **총 31개 테스트**: 100% 성공률

### QA_UI_Browser_Test.mov
- **내용**: UI 테스트 브라우저 headed모드 시연 영상

## 🎯 주요 테스트 범위

### API 테스트 (25개)
- **Positive Tests**: 정상 케이스 검증
- **Negative Tests**: 오류 처리 검증
- **Boundary Tests**: 경계값 테스트
- **Security Tests**: 보안 취약점 검증
- **Duplicate Tests**: 중복 처리 검증

### UI 테스트 (6개)
- **Registration Flow**: 회원가입 프로세스
- **Validation**: 실시간 유효성 검사
- **Error Handling**: 오류 메시지 표시
- **User Experience**: 사용자 경험 검증

## 📈 테스트 실행 환경
- **실행 환경**: Docker Container
- **테스트 프레임워크**: pytest + Playwright
- **리포트 도구**: Allure Report
- **실행 일자**: 2025년 8월

## 💡 참고사항
- 이 PDF는 실제 테스트 실행 결과를 Allure Report에서 추출한 것입니다
- 상세한 실시간 리포트는 `./run_tests.sh` 실행 후 http://localhost:9090 에서 확인 가능합니다