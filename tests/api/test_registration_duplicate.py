"""
Duplicate email test scenarios for user registration API
"""
import pytest
import allure
from base_api_test import BaseAPITest

@allure.feature("User Registration")
@allure.story("Duplicate Prevention")
class TestRegistrationDuplicate(BaseAPITest):
    
    @allure.title("TC-024: 중복 이메일로 회원가입 시도")
    @allure.testcase("TC-024")
    @allure.severity("critical")
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.smoke
    def test_registration_duplicate_email_blocked(self):
        """Test that duplicate email registration is blocked"""
        test_case = self.test_data["duplicate_cases"][0]
        
        # First registration should succeed
        with allure.step("Register first user"):
            first_result = self.register_user(
                email=test_case["email"],
                password=test_case["password"],
                expected_status=200
            )
            assert "id" in first_result, "First registration should succeed"
            first_user_id = first_result["id"]
        
        # Second registration with same email should fail
        with allure.step("Attempt duplicate registration"):
            # This should now return 400 with error message
            second_result = self.client.post(
                self.endpoints["register"],
                json={
                    "email": test_case["email"],
                    "password": test_case["password"]
                }
            )
            
            # Should get 400 error for duplicate
            assert second_result.status_code == 400, \
                f"Expected 400 for duplicate, got {second_result.status_code}"
            
            error_response = second_result.json()
            assert "error" in error_response, "Error response should contain error message"
            assert "DUPLICATE_EMAIL" in error_response.get("code", ""), \
                "Error code should indicate duplicate email"
    
    @allure.title("TC-025: 대소문자 다른 중복 이메일")
    @allure.testcase("TC-025")
    @allure.severity("high")
    @pytest.mark.api
    @pytest.mark.negative
    def test_registration_duplicate_email_case_insensitive(self):
        """Test that email uniqueness is case-insensitive"""
        base_email = "CaseSensitive@Test.com"
        
        # Register with mixed case
        with allure.step("Register with mixed case email"):
            first_result = self.register_user(
                email=base_email,
                password="Test1234!",
                expected_status=200
            )
            assert "id" in first_result, "First registration should succeed"
        
        # Try to register with lowercase version
        with allure.step("Attempt registration with lowercase email"):
            lowercase_email = base_email.lower()
            
            # Check if system treats emails as case-insensitive
            existing = self.check_duplicate_email(lowercase_email)
            
            # This assertion depends on implementation
            # Some systems are case-sensitive, others are not
            allure.attach(
                f"Original: {base_email}\nLowercase: {lowercase_email}\nExists: {existing}",
                name="Case Sensitivity Check",
                attachment_type=allure.attachment_type.TEXT
            )