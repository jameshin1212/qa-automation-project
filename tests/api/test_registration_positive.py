"""
Positive test scenarios for user registration API
"""
import pytest
import allure
import json
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
        
        # Expected request
        request_data = {
            "email": test_case["email"],
            "password": test_case["password"]
        }
        
        with allure.step(f"Request: {json.dumps(request_data, indent=2)}"):
            # Register user
            result = self.register_user(
                email=test_case["email"],
                password=test_case["password"],
                expected_status=200
            )
        
        # Expected response structure for successful registration
        with allure.step("Verify response structure and content"):
            # Verify required fields in response
            assert "id" in result, "Response must contain 'id' field"
            assert "email" in result, "Response must contain 'email' field"
            assert "password" in result, "Response must contain 'password' field (hashed)"
            assert "created_at" in result, "Response must contain 'created_at' field"
            
            # Verify field values
            assert isinstance(result["id"], int), "ID should be an integer"
            assert result["email"] == test_case["email"], f"Email should match: expected={test_case['email']}, actual={result['email']}"
            
            # Verify password is hashed (not plain text)
            assert result["password"] != test_case["password"], "Password must be hashed, not plain text"
            assert len(result["password"]) == 64, "Password should be SHA256 hash (64 characters)"
            
            # Verify timestamp format
            assert self.validate_timestamp(result["created_at"]), "created_at should be valid ISO timestamp"
            
            # Log the actual response for debugging
            allure.attach(
                json.dumps(result, indent=2),
                name="Actual Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        # Verify user was actually created in database
        with allure.step("Verify user persisted in database"):
            user = self.get_user_by_email(test_case["email"])
            assert user is not None, "User should be created in database"
            assert user["email"] == test_case["email"], "Stored email should match"
            assert user["password"] != test_case["password"], "Stored password should be hashed"
    
    @allure.title("TC-002: 이메일에 + 기호가 포함된 경우 회원가입")
    @allure.testcase("TC-002")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_email_with_plus_sign_success(self):
        """Test registration with email containing plus sign"""
        test_case = self.test_data["positive_cases"][1]
        
        # Expected request
        request_data = {
            "email": test_case["email"],  # user+tag@gmail.com
            "password": test_case["password"]
        }
        
        with allure.step(f"Request: {json.dumps(request_data, indent=2)}"):
            result = self.register_user(
                email=test_case["email"],
                password=test_case["password"],
                expected_status=200
            )
        
        # Verify response for email with plus sign
        with allure.step("Verify response accepts email with + sign"):
            assert "id" in result, "Response must contain 'id' field"
            assert "email" in result, "Response must contain 'email' field"
            assert result["email"] == test_case["email"], f"Email with + should be preserved: {test_case['email']}"
            assert "+" in result["email"], "Plus sign should be preserved in email"
            
            allure.attach(
                json.dumps(result, indent=2),
                name="Response with + email",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.title("TC-003: 한국 도메인 이메일로 회원가입")
    @allure.testcase("TC-003")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_korean_domain_email_success(self):
        """Test registration with Korean domain email"""
        test_case = self.test_data["positive_cases"][2]
        
        # Expected request with Korean domain
        request_data = {
            "email": test_case["email"],  # korean.user@naver.com
            "password": test_case["password"]
        }
        
        with allure.step(f"Request: {json.dumps(request_data, indent=2)}"):
            result = self.register_user(
                email=test_case["email"],
                password=test_case["password"],
                expected_status=200
            )
        
        # Verify Korean domain acceptance
        with allure.step("Verify response accepts Korean domain (naver.com)"):
            assert "id" in result, "Response must contain 'id' field"
            assert "email" in result, "Response must contain 'email' field"
            assert "naver.com" in result["email"], "Korean domain (naver.com) should be accepted"
            assert result["email"] == test_case["email"], f"Email should match: {test_case['email']}"
            
            allure.attach(
                json.dumps(result, indent=2),
                name="Response with Korean domain",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.title("TC-004: 긴 이메일 주소로 회원가입")
    @allure.testcase("TC-004")
    @allure.severity("medium")
    @pytest.mark.api
    @pytest.mark.positive
    def test_registration_long_email_address_success(self):
        """Test registration with long email address"""
        test_case = self.test_data["positive_cases"][3]
        
        # Expected request with long email
        request_data = {
            "email": test_case["email"],  # long.email.address.with.many.dots@example.com
            "password": test_case["password"]
        }
        
        with allure.step(f"Request with {len(test_case['email'])} character email"):
            result = self.register_user(
                email=test_case["email"],
                password=test_case["password"],
                expected_status=200
            )
        
        # Verify long email acceptance
        with allure.step("Verify response accepts long email address"):
            assert "id" in result, "Response must contain 'id' field"
            assert "email" in result, "Response must contain 'email' field"
            assert len(result["email"]) > 30, f"Long email ({len(result['email'])} chars) should be accepted"
            assert result["email"] == test_case["email"], "Long email should be stored completely"
            
            allure.attach(
                json.dumps(result, indent=2),
                name="Response with long email",
                attachment_type=allure.attachment_type.JSON
            )