"""
Generate Excel test case documentation
"""
import pandas as pd
from datetime import datetime
import os

def create_test_cases_excel():
    """Create comprehensive test case documentation in Excel"""
    
    # Test case data
    test_cases = [
        # Positive scenarios
        {"TC_ID": "TC-001", "Category": "정상 플로우", "Test_Name": "정상적인 이메일과 비밀번호로 회원가입",
         "Test_Type": "API", "Priority": "Critical", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중", 
         "Test_Steps": "1. 유효한 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: valid.user@test.com\npassword: Test1234!",
         "Expected_Result": "201 Created, 사용자 생성됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_positive.py::test_registration_valid_email_password_success"},
        
        {"TC_ID": "TC-002", "Category": "정상 플로우", "Test_Name": "이메일에 + 기호가 포함된 경우",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. + 기호가 포함된 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: user+tag@gmail.com\npassword: Secure@Pass123",
         "Expected_Result": "201 Created, + 기호 허용", "Automation_Status": "완료",
         "Test_Script": "test_registration_positive.py::test_registration_email_with_plus_sign_success"},
        
        {"TC_ID": "TC-003", "Category": "정상 플로우", "Test_Name": "한국 도메인 이메일로 회원가입",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. naver.com 도메인 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: korean.user@naver.com\npassword: Korean123!@#",
         "Expected_Result": "201 Created, 한국 도메인 허용", "Automation_Status": "완료",
         "Test_Script": "test_registration_positive.py::test_registration_korean_domain_email_success"},
        
        {"TC_ID": "TC-004", "Category": "정상 플로우", "Test_Name": "긴 이메일 주소로 회원가입",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 30자 이상 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: long.email.address.with.many.dots@example.com",
         "Expected_Result": "201 Created, 긴 이메일 허용", "Automation_Status": "완료",
         "Test_Script": "test_registration_positive.py::test_registration_long_email_address_success"},
        
        # Negative scenarios
        {"TC_ID": "TC-005", "Category": "비정상 플로우", "Test_Name": "잘못된 이메일 형식 - @ 기호 누락",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. @ 없는 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: invalid-email\npassword: Test1234!",
         "Expected_Result": "400 Bad Request, 에러 메시지", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_invalid_email_missing_at_fail"},
        
        {"TC_ID": "TC-006", "Category": "비정상 플로우", "Test_Name": "잘못된 이메일 - 로컬 파트 누락",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 로컬 파트 없는 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: @test.com\npassword: Test1234!",
         "Expected_Result": "400 Bad Request", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_invalid_email_missing_local_fail"},
        
        {"TC_ID": "TC-007", "Category": "비정상 플로우", "Test_Name": "잘못된 이메일 - 도메인 누락",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 도메인 없는 이메일 입력\n2. 유효한 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: test@\npassword: Test1234!",
         "Expected_Result": "400 Bad Request", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_invalid_email_missing_domain_fail"},
        
        {"TC_ID": "TC-008", "Category": "비정상 플로우", "Test_Name": "비밀번호가 너무 짧음",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일 입력\n2. 짧은 비밀번호 입력\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: short",
         "Expected_Result": "400 Bad Request, 최소 8자 필요", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_password_too_short_fail"},
        
        {"TC_ID": "TC-009", "Category": "비정상 플로우", "Test_Name": "비밀번호에 대문자 누락",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일 입력\n2. 대문자 없는 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: nouppercase123!",
         "Expected_Result": "400 Bad Request, 대문자 필요", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_password_missing_uppercase_fail"},
        
        {"TC_ID": "TC-010", "Category": "비정상 플로우", "Test_Name": "비밀번호에 소문자 누락",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일 입력\n2. 소문자 없는 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: NOLOWERCASE123!",
         "Expected_Result": "400 Bad Request, 소문자 필요", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_password_missing_lowercase_fail"},
        
        {"TC_ID": "TC-011", "Category": "비정상 플로우", "Test_Name": "빈 이메일 필드",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 빈 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: (empty)\npassword: Test1234!",
         "Expected_Result": "400 Bad Request, 필수 필드", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_empty_email_fail"},
        
        {"TC_ID": "TC-012", "Category": "비정상 플로우", "Test_Name": "빈 비밀번호 필드",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일\n2. 빈 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: (empty)",
         "Expected_Result": "400 Bad Request, 필수 필드", "Automation_Status": "완료",
         "Test_Script": "test_registration_negative.py::test_registration_empty_password_fail"},
        
        # Boundary tests
        {"TC_ID": "TC-013", "Category": "경계값", "Test_Name": "최소 길이 이메일",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 최소 길이 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: a@b.co\npassword: Pass123!",
         "Expected_Result": "201 Created", "Automation_Status": "완료",
         "Test_Script": "test_registration_boundary.py::test_registration_minimum_email_length_success"},
        
        {"TC_ID": "TC-014", "Category": "경계값", "Test_Name": "최소 길이 비밀번호 (8자)",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일\n2. 정확히 8자 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: Pass123!",
         "Expected_Result": "201 Created", "Automation_Status": "완료",
         "Test_Script": "test_registration_boundary.py::test_registration_minimum_password_length_success"},
        
        {"TC_ID": "TC-015", "Category": "경계값", "Test_Name": "매우 긴 이메일 주소",
         "Test_Type": "API", "Priority": "Low", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 100자 이상 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: very.long.email...@test.com",
         "Expected_Result": "201 Created 또는 길이 제한", "Automation_Status": "완료",
         "Test_Script": "test_registration_boundary.py::test_registration_very_long_email_success"},
        
        {"TC_ID": "TC-016", "Category": "경계값", "Test_Name": "매우 긴 비밀번호",
         "Test_Type": "API", "Priority": "Low", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일\n2. 100자 이상 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: VeryLongPassword...",
         "Expected_Result": "201 Created 또는 길이 제한", "Automation_Status": "완료",
         "Test_Script": "test_registration_boundary.py::test_registration_very_long_password_success"},
        
        {"TC_ID": "TC-017", "Category": "경계값", "Test_Name": "이메일 공백 처리",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 공백 포함 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: '  test@test.com  '\npassword: Test1234!",
         "Expected_Result": "공백 제거 후 처리", "Automation_Status": "완료",
         "Test_Script": "test_registration_boundary.py::test_registration_email_with_spaces_trimmed"},
        
        # Security tests
        {"TC_ID": "TC-018", "Category": "보안", "Test_Name": "SQL Injection - 이메일",
         "Test_Type": "API", "Priority": "Critical", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. SQL Injection 시도\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: admin'--@test.com\npassword: Test1234!",
         "Expected_Result": "400 Bad Request, 차단됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_sql_injection_email_blocked"},
        
        {"TC_ID": "TC-019", "Category": "보안", "Test_Name": "SQL Injection - 비밀번호",
         "Test_Type": "API", "Priority": "Critical", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일\n2. SQL Injection 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: ' OR '1'='1",
         "Expected_Result": "400 Bad Request, 차단됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_sql_injection_password_blocked"},
        
        {"TC_ID": "TC-020", "Category": "보안", "Test_Name": "XSS 공격 - 이메일",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. XSS 스크립트 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: <script>alert('XSS')</script>@test.com",
         "Expected_Result": "400 Bad Request, 차단됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_xss_email_sanitized"},
        
        {"TC_ID": "TC-021", "Category": "보안", "Test_Name": "XSS 공격 - 비밀번호",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 이메일\n2. XSS 스크립트 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: test@test.com\npassword: <script>alert('XSS')</script>",
         "Expected_Result": "400 Bad Request, 차단됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_xss_password_handled"},
        
        {"TC_ID": "TC-022", "Category": "보안", "Test_Name": "Path Traversal 시도",
         "Test_Type": "API", "Priority": "Medium", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. Path traversal 이메일\n2. 유효한 비밀번호\n3. 회원가입 요청",
         "Test_Data": "email: ../../../etc/passwd@test.com",
         "Expected_Result": "400 Bad Request, 차단됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_path_traversal_email_blocked"},
        
        {"TC_ID": "TC-023", "Category": "보안", "Test_Name": "비밀번호 암호화 확인",
         "Test_Type": "API", "Priority": "Critical", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 유효한 회원가입\n2. 저장된 데이터 확인\n3. 비밀번호 평문 여부 검증",
         "Test_Data": "email: security.test@example.com\npassword: SecurePass123!",
         "Expected_Result": "비밀번호 암호화됨", "Automation_Status": "완료",
         "Test_Script": "test_registration_security.py::test_registration_password_not_stored_plain"},
        
        # Duplicate
        {"TC_ID": "TC-024", "Category": "중복 방지", "Test_Name": "중복 이메일 차단",
         "Test_Type": "API", "Priority": "Critical", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. 첫 번째 회원가입\n2. 동일 이메일로 재시도\n3. 중복 확인",
         "Test_Data": "email: duplicate@test.com\npassword: Test1234!",
         "Expected_Result": "409 Conflict 또는 차단", "Automation_Status": "완료",
         "Test_Script": "test_registration_duplicate.py::test_registration_duplicate_email_blocked"},
        
        {"TC_ID": "TC-025", "Category": "중복 방지", "Test_Name": "대소문자 다른 중복 이메일",
         "Test_Type": "API", "Priority": "High", "Test_Method": "API_Auto",
         "Precondition": "Mock 서버 실행 중",
         "Test_Steps": "1. Mixed case 이메일 등록\n2. Lowercase로 재시도\n3. 중복 확인",
         "Test_Data": "email: CaseSensitive@Test.com",
         "Expected_Result": "대소문자 구분 확인", "Automation_Status": "완료",
         "Test_Script": "test_registration_duplicate.py::test_registration_duplicate_email_case_insensitive"},
        
        # UI Tests
        {"TC_ID": "TC-026", "Category": "UI", "Test_Name": "UI - 정상 회원가입 플로우",
         "Test_Type": "UI", "Priority": "Critical", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 회원가입 페이지 접속\n2. 유효한 정보 입력\n3. 제출 버튼 클릭",
         "Test_Data": "유효한 이메일과 비밀번호",
         "Expected_Result": "성공 메시지 표시", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_registration_happy_path"},
        
        {"TC_ID": "TC-027", "Category": "UI", "Test_Name": "UI - 잘못된 이메일 에러",
         "Test_Type": "UI", "Priority": "High", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 잘못된 이메일 입력\n2. 에러 메시지 확인",
         "Test_Data": "invalid-email",
         "Expected_Result": "이메일 형식 에러 표시", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_invalid_email_format_error"},
        
        {"TC_ID": "TC-028", "Category": "UI", "Test_Name": "UI - 짧은 비밀번호 에러",
         "Test_Type": "UI", "Priority": "High", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 짧은 비밀번호 입력\n2. 제출\n3. 에러 확인",
         "Test_Data": "password: short",
         "Expected_Result": "비밀번호 길이 에러", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_short_password_error"},
        
        {"TC_ID": "TC-029", "Category": "UI", "Test_Name": "UI - 중복 이메일 에러",
         "Test_Type": "UI", "Priority": "High", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 이미 등록된 이메일 입력\n2. 제출\n3. 에러 확인",
         "Test_Data": "duplicate@test.com",
         "Expected_Result": "중복 이메일 에러", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_duplicate_email_error"},
        
        {"TC_ID": "TC-030", "Category": "UI", "Test_Name": "UI - 필수 필드 검증",
         "Test_Type": "UI", "Priority": "Medium", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 빈 폼 제출\n2. 필수 필드 검증",
         "Test_Data": "empty fields",
         "Expected_Result": "필수 필드 에러", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_required_fields_validation"},
        
        {"TC_ID": "TC-031", "Category": "UI", "Test_Name": "UI - 실시간 입력 검증",
         "Test_Type": "UI", "Priority": "Low", "Test_Method": "UI_Auto",
         "Precondition": "웹 페이지 접속 가능",
         "Test_Steps": "1. 잘못된 입력\n2. 포커스 이동\n3. 실시간 에러 확인",
         "Test_Data": "various inputs",
         "Expected_Result": "실시간 검증 동작", "Automation_Status": "완료",
         "Test_Script": "test_registration_ui.py::test_ui_realtime_validation_feedback"}
    ]
    
    # Convert to DataFrame
    df_test_cases = pd.DataFrame(test_cases)
    
    # Test summary data
    summary_data = {
        "Category": ["정상 플로우", "비정상 플로우", "경계값", "보안", "중복 방지", "UI", "합계"],
        "API Tests": [4, 8, 5, 6, 2, 0, 25],
        "UI Tests": [1, 3, 0, 0, 1, 6, 6],
        "Total": [5, 11, 5, 6, 3, 6, 31],
        "Automated": [5, 11, 5, 6, 3, 6, 31],
        "Manual": [0, 0, 0, 0, 0, 0, 0],
        "Coverage": ["100%", "100%", "100%", "100%", "100%", "100%", "100%"]
    }
    df_summary = pd.DataFrame(summary_data)
    
    # Test execution tracking
    execution_data = {
        "TC_ID": [f"TC-{str(i).zfill(3)}" for i in range(1, 32)],
        "Last_Execution": ["Not Executed"] * 31,
        "Last_Result": ["N/A"] * 31,
        "Execution_Time": ["N/A"] * 31,
        "Defects_Found": [0] * 31,
        "Notes": [""] * 31
    }
    df_execution = pd.DataFrame(execution_data)
    
    # Create Excel file
    output_file = "test_cases.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write each dataframe to different sheets
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        df_test_cases.to_excel(writer, sheet_name='Test Cases', index=False)
        df_execution.to_excel(writer, sheet_name='Execution Tracking', index=False)
        
        # Auto-adjust column widths
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"Test cases Excel file created: {output_file}")
    print(f"Total test cases: {len(test_cases)}")
    print(f"- API Tests: {sum(1 for tc in test_cases if tc['Test_Type'] == 'API')}")
    print(f"- UI Tests: {sum(1 for tc in test_cases if tc['Test_Type'] == 'UI')}")

if __name__ == "__main__":
    create_test_cases_excel()