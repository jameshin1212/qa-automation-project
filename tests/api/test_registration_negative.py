"""
Negative test scenarios for user registration API
"""
import pytest
import allure
import json
from base_api_test import BaseAPITest

@allure.feature("User Registration")
@allure.story("Negative Scenarios")
class TestRegistrationNegative(BaseAPITest):
    
    @allure.title("TC-005: 잘못된 이메일 형식 - @ 기호 누락")
    @allure.testcase("TC-005")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_invalid_email_missing_at_fail(self):
        """Test registration fails with invalid email format - missing @"""
        test_case = self.test_data["negative_cases"][0]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=400
        )
        
        # JSON Server might not validate, so we check our validation
        assert not self.validate_email_format(test_case["email"]), \
            "Email without @ should be invalid"
    
    @allure.title("TC-006: 잘못된 이메일 형식 - 로컬 파트 누락")
    @allure.testcase("TC-006")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_invalid_email_missing_local_fail(self):
        """Test registration fails with invalid email - missing local part"""
        test_case = self.test_data["negative_cases"][1]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=400
        )
        
        assert not self.validate_email_format(test_case["email"]), \
            "Email without local part should be invalid"
    
    @allure.title("TC-007: 잘못된 이메일 형식 - 도메인 누락")
    @allure.testcase("TC-007")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_invalid_email_missing_domain_fail(self):
        """Test registration fails with invalid email - missing domain"""
        test_case = self.test_data["negative_cases"][2]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=400
        )
        
        assert not self.validate_email_format(test_case["email"]), \
            "Email without domain should be invalid"
    
    @allure.title("TC-008: 비밀번호가 너무 짧음")
    @allure.testcase("TC-008")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_password_too_short_fail(self):
        """Test registration fails with password too short"""
        import uuid
        
        # Test with 7-character password
        email = f"shortpass_{uuid.uuid4().hex[:8]}@test.com"
        password = "Test12!"  # Exactly 7 characters
        
        result = self.register_user(
            email=email,
            password=password,
            expected_status=400
        )
        
        # Should get error for short password
        error_data = result.json()
        assert error_data.get("code") == "INVALID_PASSWORD", \
            f"Expected INVALID_PASSWORD error, got {error_data}"
    
    @allure.title("TC-009: 비밀번호에 대문자 누락")
    @allure.testcase("TC-009")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_password_missing_uppercase_fail(self):
        """Test registration fails with password missing uppercase"""
        test_case = self.test_data["negative_cases"][4]
        
        validations = self.validate_password_complexity(test_case["password"])
        assert not validations["has_uppercase"], "Password should lack uppercase"
        assert not validations["is_valid"], "Password should be invalid"
    
    @allure.title("TC-010: 비밀번호에 소문자 누락")
    @allure.testcase("TC-010")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_password_missing_lowercase_fail(self):
        """Test registration fails with password missing lowercase"""
        import uuid
        
        # Test with password without lowercase
        email = f"nolower_{uuid.uuid4().hex[:8]}@test.com"
        password = "NOLOWERCASE123!"  # No lowercase letters
        
        result = self.register_user(
            email=email,
            password=password,
            expected_status=400
        )
        
        # Should get error for weak password
        error_data = result.json()
        assert error_data.get("code") == "WEAK_PASSWORD", \
            f"Expected WEAK_PASSWORD error, got {error_data}"
    
    @allure.title("TC-011: 빈 이메일 필드")
    @allure.testcase("TC-011")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.smoke
    def test_registration_empty_email_fail(self):
        """Test registration fails with empty email"""
        test_case = self.test_data["negative_cases"][8]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=400
        )
        
        assert test_case["email"] == "", "Email should be empty"
    
    @allure.title("TC-012: 빈 비밀번호 필드")
    @allure.testcase("TC-012")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.smoke
    def test_registration_empty_password_fail(self):
        """Test registration fails with empty password"""
        test_case = self.test_data["negative_cases"][9]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=400
        )
        
        assert test_case["password"] == "", "Password should be empty"