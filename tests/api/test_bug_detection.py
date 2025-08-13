"""
Bug Detection Tests - Educational QA Demonstration
These tests are designed to detect intentional bugs in the system.
They will FAIL when bugs are present, demonstrating QA value.
"""
import pytest
import allure
import json
from base_api_test import BaseAPITest

@allure.feature("Bug Detection")
@allure.story("System Validation Issues")
class TestBugDetection(BaseAPITest):
    
    @allure.title("BUG-TC-008: 비밀번호 최소 길이 검증 실패")
    @allure.testcase("BUG-TC-008")
    @allure.severity("critical")
    @allure.issue("SEC-001", "Password Policy Violation")
    @pytest.mark.api
    @pytest.mark.bug_detection
    def test_bug_short_password_accepted(self):
        """Detect bug: System incorrectly accepts 7-character passwords
        
        Expected: 400 Bad Request - "비밀번호는 최소 8자 이상이어야 합니다."
        Actual Bug: 200 OK - Password accepted
        Impact: Security policy violation, weak passwords allowed
        """
        # Test with exactly 7 characters (should fail but doesn't due to bug)
        test_email = "shortpass@test.com"
        test_password = "Test12!"  # Exactly 7 characters
        
        with allure.step("Testing 7-character password (should be rejected)"):
            response = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_email,
                    "password": test_password
                }
            )
            
            allure.attach(
                json.dumps({
                    "email": test_email,
                    "password": test_password,
                    "password_length": len(test_password)
                }, indent=2),
                name="Request Data",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Check if bug exists
            if response.status_code == 200:
                # Bug detected - password validation bypassed
                bug_report = {
                    "bug_id": "BUG-TC-008",
                    "severity": "HIGH",
                    "description": "7-character password accepted instead of being rejected",
                    "expected_status": 400,
                    "actual_status": 200,
                    "expected_error": "비밀번호는 최소 8자 이상이어야 합니다.",
                    "actual_response": response.json(),
                    "recommendation": "Fix password length validation in middleware.js line 51-56"
                }
                
                allure.attach(
                    json.dumps(bug_report, indent=2),
                    name="🐛 Bug Report",
                    attachment_type=allure.attachment_type.JSON
                )
                
                pytest.fail(f"BUG DETECTED: Password with {len(test_password)} chars was accepted (minimum should be 8)")
            
            # If we get here, bug is fixed
            assert response.status_code == 400, "Short password should be rejected"
            error_data = response.json()
            assert error_data.get("code") == "INVALID_PASSWORD"
    
    @allure.title("BUG-TC-010: 비밀번호 복잡도 검증 우회")
    @allure.testcase("BUG-TC-010")
    @allure.severity("high")
    @allure.issue("SEC-002", "Password Complexity Bypass")
    @pytest.mark.api
    @pytest.mark.bug_detection
    def test_bug_no_lowercase_accepted(self):
        """Detect bug: System accepts password without lowercase letters
        
        Expected: 400 Bad Request - "비밀번호는 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다."
        Actual Bug: 200 OK - Password accepted
        Impact: Weak password policy enforcement
        """
        test_email = "nolowercase@test.com"
        test_password = "NOLOWERCASE123!"  # No lowercase letters
        
        with allure.step("Testing password without lowercase (should be rejected)"):
            response = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_email,
                    "password": test_password
                }
            )
            
            # Check if bug exists
            if response.status_code == 200:
                # Bug detected - complexity validation bypassed
                bug_report = {
                    "bug_id": "BUG-TC-010",
                    "severity": "HIGH",
                    "description": "Password without lowercase letters accepted",
                    "expected_status": 400,
                    "actual_status": 200,
                    "expected_error": "비밀번호는 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.",
                    "password_analysis": {
                        "has_uppercase": True,
                        "has_lowercase": False,  # Missing!
                        "has_number": True,
                        "has_special": True
                    },
                    "recommendation": "Fix password complexity validation in middleware.js line 73-77"
                }
                
                allure.attach(
                    json.dumps(bug_report, indent=2),
                    name="🐛 Bug Report",
                    attachment_type=allure.attachment_type.JSON
                )
                
                pytest.fail("BUG DETECTED: Password without lowercase letters was accepted")
            
            # If we get here, bug is fixed
            assert response.status_code == 400, "Password without lowercase should be rejected"
            error_data = response.json()
            assert error_data.get("code") == "WEAK_PASSWORD"
    
    @allure.title("BUG-TC-020: XSS 방어 우회")
    @allure.testcase("BUG-TC-020")
    @allure.severity("critical")
    @allure.issue("SEC-003", "XSS Vulnerability")
    @pytest.mark.api
    @pytest.mark.bug_detection
    @pytest.mark.security
    def test_bug_xss_bypass(self):
        """Detect bug: Specific XSS pattern bypasses security validation
        
        Expected: 400 Bad Request - "이메일에 허용되지 않는 문자가 포함되어 있습니다."
        Actual Bug: 200 OK - XSS pattern accepted
        Impact: Potential XSS vulnerability, security breach
        """
        test_email = "<script>alert('XSS')</script>@test.com"
        test_password = "SecurePass123!"
        
        with allure.step("Testing XSS pattern in email (should be blocked)"):
            response = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_email,
                    "password": test_password
                }
            )
            
            # Check if bug exists
            if response.status_code == 200:
                # Bug detected - XSS validation bypassed
                bug_report = {
                    "bug_id": "BUG-TC-020",
                    "severity": "CRITICAL",
                    "description": "XSS script pattern accepted in email field",
                    "expected_status": 400,
                    "actual_status": 200,
                    "expected_error": "이메일에 허용되지 않는 문자가 포함되어 있습니다.",
                    "malicious_input": test_email,
                    "security_impact": "Potential XSS attack vector",
                    "recommendation": "Strengthen XSS filtering in middleware.js line 35-40"
                }
                
                allure.attach(
                    json.dumps(bug_report, indent=2),
                    name="🚨 Critical Security Bug",
                    attachment_type=allure.attachment_type.JSON
                )
                
                # Check if malicious content was stored
                users = self.client.get(self.endpoints["users"]).json()
                xss_stored = any("<script>" in user.get("email", "") for user in users)
                
                if xss_stored:
                    pytest.fail("CRITICAL BUG: XSS pattern was stored in database!")
                else:
                    pytest.fail("BUG DETECTED: XSS pattern was accepted (not blocked)")
            
            # If we get here, bug is fixed
            assert response.status_code == 400, "XSS pattern should be blocked"
            error_data = response.json()
            assert error_data.get("code") == "INVALID_EMAIL"
    
    @allure.title("BUG-TC-024: 중복 이메일 허용")
    @allure.testcase("BUG-TC-024")
    @allure.severity("high")
    @allure.issue("DATA-001", "Unique Constraint Violation")
    @pytest.mark.api
    @pytest.mark.bug_detection
    def test_bug_duplicate_email_allowed(self):
        """Detect bug: System allows duplicate email registration
        
        Expected: 400 Bad Request - "이미 등록된 이메일입니다."
        Actual Bug: 200 OK - Duplicate allowed
        Impact: Data integrity violation, multiple accounts with same email
        """
        test_email = "duplicate@test.com"
        test_password = "ValidPass123!"
        
        # First registration - should succeed
        with allure.step("First registration (should succeed)"):
            first_response = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_email,
                    "password": test_password
                }
            )
            
            if first_response.status_code != 200:
                pytest.skip("First registration failed, cannot test duplicate")
            
            first_user_id = first_response.json().get("id")
        
        # Second registration - should fail but doesn't due to bug
        with allure.step("Duplicate registration attempt (should be blocked)"):
            duplicate_response = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_email,
                    "password": test_password
                }
            )
            
            # Check if bug exists
            if duplicate_response.status_code == 200:
                # Bug detected - duplicate allowed
                second_user_id = duplicate_response.json().get("id")
                
                bug_report = {
                    "bug_id": "BUG-TC-024",
                    "severity": "HIGH",
                    "description": "Duplicate email registration allowed",
                    "expected_status": 400,
                    "actual_status": 200,
                    "expected_error": "이미 등록된 이메일입니다.",
                    "first_user_id": first_user_id,
                    "duplicate_user_id": second_user_id,
                    "data_integrity_impact": "Multiple users with same email",
                    "recommendation": "Fix duplicate check in middleware.js line 94-105"
                }
                
                allure.attach(
                    json.dumps(bug_report, indent=2),
                    name="🐛 Bug Report",
                    attachment_type=allure.attachment_type.JSON
                )
                
                # Verify duplicates in database
                users = self.client.get(self.endpoints["users"]).json()
                duplicate_count = sum(1 for user in users if user.get("email") == test_email)
                
                pytest.fail(f"BUG DETECTED: Duplicate email allowed ({duplicate_count} users with same email)")
            
            # If we get here, bug is fixed (duplicate correctly blocked)
            assert duplicate_response.status_code == 400, "Duplicate email should be blocked"
            error_data = duplicate_response.json()
            assert error_data.get("code") == "DUPLICATE_EMAIL"
    
    @allure.title("Bug Detection Summary")
    @pytest.mark.api
    @pytest.mark.bug_detection
    def test_bug_summary(self):
        """Generate summary of all detected bugs"""
        # This test always passes but generates a summary report
        bugs_expected = [
            "BUG-TC-008: Short password validation failure",
            "BUG-TC-010: Password complexity bypass",
            "BUG-TC-020: XSS validation bypass",
            "BUG-TC-024: Duplicate email allowed"
        ]
        
        summary = {
            "total_bugs_injected": 4,
            "bugs_list": bugs_expected,
            "purpose": "Educational QA demonstration",
            "note": "These bugs are intentionally injected to demonstrate QA testing value"
        }
        
        allure.attach(
            json.dumps(summary, indent=2),
            name="Bug Detection Test Suite Summary",
            attachment_type=allure.attachment_type.JSON
        )
        
        assert True, "Summary generated"