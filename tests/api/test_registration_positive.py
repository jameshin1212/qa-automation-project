"""
Positive test scenarios for user registration API
"""
import pytest
import allure
from base_api_test import BaseAPITest

@allure.feature("User Registration")
@allure.story("Positive Scenarios")
class TestRegistrationPositive(BaseAPITest):
    
    @allure.title("TC-001: 정상적인 이메일과 비밀번호로 회원가입")
    @allure.testcase("TC-001")
    @allure.severity("critical")
    @pytest.mark.api
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_registration_valid_email_password_success(self):
        """Test successful registration with valid email and password"""
        test_case = self.test_data["positive_cases"][0]
        
        # Register user
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        # Verify response structure
        assert "id" in result, "Response should contain user ID"
        assert "email" in result, "Response should contain email"
        assert result["email"] == test_case["email"], "Email should match"
        
        # Verify user was actually created
        user = self.get_user_by_email(test_case["email"])
        assert user is not None, "User should be created in database"
        assert user["email"] == test_case["email"], "Stored email should match"
    
    @allure.title("TC-002: 이메일에 + 기호가 포함된 경우 회원가입")
    @allure.testcase("TC-002")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_email_with_plus_sign_success(self):
        """Test registration with email containing plus sign"""
        test_case = self.test_data["positive_cases"][1]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Response should contain user ID"
        assert result["email"] == test_case["email"], "Email with + should be accepted"
    
    @allure.title("TC-003: 한국 도메인 이메일로 회원가입")
    @allure.testcase("TC-003")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_korean_domain_email_success(self):
        """Test registration with Korean domain email"""
        test_case = self.test_data["positive_cases"][2]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Response should contain user ID"
        assert "naver.com" in result["email"], "Korean domain should be accepted"
    
    @allure.title("TC-004: 긴 이메일 주소로 회원가입")
    @allure.testcase("TC-004")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_long_email_address_success(self):
        """Test registration with long email address"""
        test_case = self.test_data["positive_cases"][3]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Response should contain user ID"
        assert len(result["email"]) > 30, "Long email should be accepted"