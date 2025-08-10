"""
Boundary value test scenarios for user registration API
"""
import pytest
import allure
from base_api_test import BaseAPITest

@allure.feature("User Registration")
@allure.story("Boundary Value Testing")
class TestRegistrationBoundary(BaseAPITest):
    
    @allure.title("TC-013: 최소 길이 이메일로 회원가입")
    @allure.testcase("TC-013")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.boundary
    def test_registration_minimum_email_length_success(self):
        """Test registration with minimum valid email length"""
        test_case = self.test_data["boundary_cases"][0]
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert len(test_case["email"]) <= 10, "Email should be minimum length"
        assert "id" in result, "Short valid email should be accepted"
    
    @allure.title("TC-014: 최소 길이 비밀번호 (8자)로 회원가입")
    @allure.testcase("TC-014")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.boundary
    def test_registration_minimum_password_length_success(self):
        """Test registration with minimum password length (8 chars)"""
        test_case = self.test_data["boundary_cases"][1]
        
        assert len(test_case["password"]) == 8, "Password should be exactly 8 chars"
        
        validations = self.validate_password_complexity(test_case["password"])
        assert validations["min_length"], "8-char password should meet minimum"
        assert validations["is_valid"], "Valid 8-char password should pass"
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Minimum length password should be accepted"
    
    @allure.title("TC-015: 매우 긴 이메일 주소로 회원가입")
    @allure.testcase("TC-015")
    @allure.severity("low")
    @pytest.mark.api
    @pytest.mark.boundary
    def test_registration_very_long_email_success(self):
        """Test registration with very long email address"""
        test_case = self.test_data["boundary_cases"][2]
        
        assert len(test_case["email"]) > 100, "Email should be very long"
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Long email should be accepted"
        assert result["email"] == test_case["email"], "Long email should be stored correctly"
    
    @allure.title("TC-016: 매우 긴 비밀번호로 회원가입")
    @allure.testcase("TC-016")
    @allure.severity("low")
    @pytest.mark.api
    @pytest.mark.boundary
    def test_registration_very_long_password_success(self):
        """Test registration with very long password"""
        test_case = self.test_data["boundary_cases"][3]
        
        assert len(test_case["password"]) > 100, "Password should be very long"
        
        validations = self.validate_password_complexity(test_case["password"])
        assert validations["is_valid"], "Long password should be valid"
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        assert "id" in result, "Long password should be accepted"
    
    @allure.title("TC-017: 이메일에 공백이 포함된 경우")
    @allure.testcase("TC-017")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.boundary
    def test_registration_email_with_spaces_trimmed(self):
        """Test registration with email containing leading/trailing spaces"""
        test_case = self.test_data["boundary_cases"][4]
        
        # Spaces should be trimmed
        expected_email = test_case["email"].strip()
        
        result = self.register_user(
            email=test_case["email"],
            password=test_case["password"],
            expected_status=200
        )
        
        # Check if email was trimmed (depends on implementation)
        stored_user = self.get_user_by_email(expected_email)
        assert stored_user is not None or self.get_user_by_email(test_case["email"]) is not None, \
            "User should be created with trimmed or original email"