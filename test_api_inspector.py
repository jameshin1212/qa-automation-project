#!/usr/bin/env python3
"""
API Test Case Inspector
각 API 테스트케이스의 Request와 Response를 확인하는 스크립트
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any, Tuple
import uuid
# Try to import colorama for colored output, fallback to no colors
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    # Create dummy color classes if colorama is not available
    class Fore:
        CYAN = YELLOW = GREEN = MAGENTA = BLUE = RED = ""
        RESET = ""
    class Style:
        RESET_ALL = ""
    HAS_COLOR = False

class APITestInspector:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}{title:^80}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def print_test_case(self, tc_id: str, description: str):
        """Print test case information"""
        print(f"{Fore.GREEN}[{tc_id}] {description}{Style.RESET_ALL}")
        
    def print_request(self, method: str, url: str, data: Dict[str, Any] = None):
        """Print request details"""
        print(f"\n{Fore.MAGENTA}📤 REQUEST:")
        print(f"  Method: {method}")
        print(f"  URL: {url}")
        if data:
            print(f"  Body: {json.dumps(data, indent=4)}")
    
    def print_response(self, response: requests.Response):
        """Print response details"""
        print(f"\n{Fore.BLUE}📥 RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Headers: {dict(response.headers)}")
        try:
            body = response.json()
            print(f"  Body: {json.dumps(body, indent=4)}")
        except:
            print(f"  Body: {response.text}")
    
    def print_validation(self, passed: bool, message: str):
        """Print validation result"""
        if passed:
            print(f"{Fore.GREEN}  ✅ {message}")
        else:
            print(f"{Fore.RED}  ❌ {message}")
    
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> requests.Response:
        """Make HTTP request and return response"""
        url = f"{self.base_url}{endpoint}"
        
        if method == "POST":
            response = self.session.post(url, json=data)
        elif method == "GET":
            response = self.session.get(url)
        else:
            response = self.session.request(method, url, json=data)
            
        return response
    
    def test_tc001_valid_registration(self):
        """TC-001: 정상적인 이메일과 비밀번호로 회원가입"""
        self.print_test_case("TC-001", "정상적인 이메일과 비밀번호로 회원가입")
        
        data = {
            "email": f"test.user_{uuid.uuid4().hex[:8]}@example.com",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        self.print_validation(response.status_code == 200, f"Status Code: {response.status_code} (Expected: 200)")
        if response.status_code == 200:
            body = response.json()
            self.print_validation("id" in body, "Response contains 'id' field")
            self.print_validation("email" in body, "Response contains 'email' field")
            self.print_validation("password" in body, "Response contains 'password' field")
            self.print_validation(body.get("password") != data["password"], "Password is hashed")
        
        return response.status_code == 200
    
    def test_tc002_email_with_plus(self):
        """TC-002: 이메일에 + 기호가 포함된 경우"""
        self.print_test_case("TC-002", "이메일에 + 기호가 포함된 경우 회원가입")
        
        data = {
            "email": f"user+tag_{uuid.uuid4().hex[:8]}@gmail.com",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        self.print_validation(response.status_code == 200, f"Status Code: {response.status_code} (Expected: 200)")
        if response.status_code == 200:
            body = response.json()
            self.print_validation("+" in body.get("email", ""), "Plus sign preserved in email")
        
        return response.status_code == 200
    
    def test_tc003_korean_domain(self):
        """TC-003: 한국 도메인 이메일로 회원가입"""
        self.print_test_case("TC-003", "한국 도메인 이메일로 회원가입")
        
        data = {
            "email": f"korean.user_{uuid.uuid4().hex[:8]}@naver.com",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        self.print_validation(response.status_code == 200, f"Status Code: {response.status_code} (Expected: 200)")
        if response.status_code == 200:
            body = response.json()
            self.print_validation("naver.com" in body.get("email", ""), "Korean domain accepted")
        
        return response.status_code == 200
    
    def test_tc005_invalid_email_no_at(self):
        """TC-005: 잘못된 이메일 형식 - @ 기호 누락"""
        self.print_test_case("TC-005", "잘못된 이메일 형식 - @ 기호 누락")
        
        data = {
            "email": "invalid.email.test.com",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        self.print_validation(response.status_code == 400, f"Status Code: {response.status_code} (Expected: 400)")
        
        return response.status_code == 400
    
    def test_tc008_password_too_short(self):
        """TC-008: 비밀번호가 너무 짧음 (BUG_SHORT_PASSWORD)"""
        self.print_test_case("TC-008", "비밀번호가 너무 짧음 [🐛 BUG Expected]")
        
        data = {
            "email": f"shortpass_{uuid.uuid4().hex[:8]}@test.com",
            "password": "Test12!"  # 7 characters
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        if response.status_code == 200:
            self.print_validation(True, f"🐛 BUG DETECTED: Short password accepted (Status: {response.status_code})")
        else:
            self.print_validation(False, f"Bug not active: Short password rejected (Status: {response.status_code})")
        
        return response.status_code
    
    def test_tc010_password_no_lowercase(self):
        """TC-010: 비밀번호에 소문자 누락 (BUG_NO_LOWERCASE)"""
        self.print_test_case("TC-010", "비밀번호에 소문자 누락 [🐛 BUG Expected]")
        
        data = {
            "email": f"nolower_{uuid.uuid4().hex[:8]}@test.com",
            "password": "NOLOWERCASE123!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        if response.status_code == 200:
            self.print_validation(True, f"🐛 BUG DETECTED: No lowercase password accepted (Status: {response.status_code})")
        else:
            self.print_validation(False, f"Bug not active: No lowercase password rejected (Status: {response.status_code})")
        
        return response.status_code
    
    def test_tc018_sql_injection(self):
        """TC-018: SQL Injection 시도"""
        self.print_test_case("TC-018", "SQL Injection 시도 - 이메일 필드")
        
        data = {
            "email": "test@test.com' OR '1'='1",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        self.print_validation(response.status_code == 400, f"SQL Injection blocked (Status: {response.status_code})")
        
        return response.status_code == 400
    
    def test_tc020_xss_bypass(self):
        """TC-020: XSS 공격 시도 (BUG_XSS_BYPASS)"""
        self.print_test_case("TC-020", "XSS 공격 시도 [🐛 BUG Expected]")
        
        data = {
            "email": "<script>alert('XSS')</script>@test.com",
            "password": "Test1234!"
        }
        
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response = self.make_request("POST", "/api/register", data)
        self.print_response(response)
        
        # Validations
        if response.status_code == 200:
            self.print_validation(True, f"🐛 BUG DETECTED: XSS pattern accepted (Status: {response.status_code})")
        else:
            self.print_validation(False, f"Bug not active: XSS pattern blocked (Status: {response.status_code})")
        
        return response.status_code
    
    def test_tc024_duplicate_email(self):
        """TC-024: 중복 이메일로 회원가입 시도 (BUG_DUPLICATE_ALLOW)"""
        self.print_test_case("TC-024", "중복 이메일로 회원가입 시도 [🐛 BUG Expected]")
        
        email = f"duplicate_{uuid.uuid4().hex[:8]}@test.com"
        data = {
            "email": email,
            "password": "Test1234!"
        }
        
        # First registration
        print(f"\n{Fore.CYAN}[첫 번째 등록 시도]")
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response1 = self.make_request("POST", "/api/register", data)
        self.print_response(response1)
        
        # Second registration with same email
        print(f"\n{Fore.CYAN}[두 번째 등록 시도 - 동일 이메일]")
        self.print_request("POST", f"{self.base_url}/api/register", data)
        response2 = self.make_request("POST", "/api/register", data)
        self.print_response(response2)
        
        # Validations
        if response2.status_code == 200:
            self.print_validation(True, f"🐛 BUG DETECTED: Duplicate email accepted (Status: {response2.status_code})")
        else:
            self.print_validation(False, f"Bug not active: Duplicate email blocked (Status: {response2.status_code})")
        
        return response2.status_code
    
    def run_all_tests(self):
        """Run all test cases"""
        self.print_header("API Test Case Inspector")
        print(f"Base URL: {self.base_url}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check server connectivity
        print(f"\n{Fore.YELLOW}Checking server connectivity...")
        try:
            response = self.session.get(f"{self.base_url}/api/users")
            print(f"{Fore.GREEN}✅ Server is running{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Server is not accessible: {e}{Style.RESET_ALL}")
            return
        
        # Positive test cases
        self.print_header("POSITIVE TEST CASES")
        self.test_tc001_valid_registration()
        time.sleep(0.5)
        self.test_tc002_email_with_plus()
        time.sleep(0.5)
        self.test_tc003_korean_domain()
        
        # Negative test cases
        self.print_header("NEGATIVE TEST CASES")
        self.test_tc005_invalid_email_no_at()
        time.sleep(0.5)
        self.test_tc008_password_too_short()
        time.sleep(0.5)
        self.test_tc010_password_no_lowercase()
        
        # Security test cases
        self.print_header("SECURITY TEST CASES")
        self.test_tc018_sql_injection()
        time.sleep(0.5)
        self.test_tc020_xss_bypass()
        
        # Duplicate test cases
        self.print_header("DUPLICATE TEST CASES")
        self.test_tc024_duplicate_email()
        
        # Summary
        self.print_header("TEST EXECUTION SUMMARY")
        print(f"{Fore.CYAN}Total test cases executed: 9")
        print(f"{Fore.YELLOW}Educational bugs tested: 4 (TC-008, TC-010, TC-020, TC-024)")
        print(f"\n{Fore.GREEN}Test inspection completed successfully!{Style.RESET_ALL}")

def main():
    # Check if custom URL is provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    
    # Create inspector and run tests
    inspector = APITestInspector(base_url)
    inspector.run_all_tests()

if __name__ == "__main__":
    main()