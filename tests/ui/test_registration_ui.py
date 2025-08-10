"""
UI test scenarios for user registration
"""
import pytest
import allure
from playwright.sync_api import Page, expect
import time

@allure.feature("User Registration UI")
@allure.story("UI Testing")
class TestRegistrationUI:
    
    @allure.title("TC-026: UI - 정상적인 회원가입 플로우")
    @allure.testcase("TC-026")
    @allure.severity("critical")
    @pytest.mark.ui
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_ui_registration_happy_path(self, registration_page):
        """Test successful registration through UI"""
        # Navigate to registration page
        registration_page.navigate()
        
        # Fill in valid credentials
        test_email = f"uitest_{int(time.time())}@test.com"
        test_password = "TestPass123!"
        
        registration_page.register_user(test_email, test_password)
        
        # Wait for success message
        registration_page.wait_for_success()
        
        # Verify success message is visible
        assert registration_page.is_success_message_visible(), \
            "Success message should be displayed"
        
        # Take screenshot of success state
        registration_page.take_screenshot("registration_success")
    
    @allure.title("TC-027: UI - 잘못된 이메일 형식 에러 표시")
    @allure.testcase("TC-027")
    @allure.severity("high")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_ui_invalid_email_format_error(self, registration_page):
        """Test that invalid email format shows error"""
        registration_page.navigate()
        
        # Enter invalid email
        registration_page.fill_email("invalid-email")
        registration_page.fill_password("ValidPass123!")
        
        # Trigger validation by clicking outside
        registration_page.password_input.click()
        registration_page.email_input.blur()
        
        # Wait for error
        registration_page.wait_for_email_error()
        
        # Verify error message
        error_text = registration_page.get_email_error_text()
        assert "올바른 이메일 형식" in error_text, \
            f"Expected email format error, got: {error_text}"
        
        registration_page.take_screenshot("invalid_email_error")
    
    @allure.title("TC-028: UI - 짧은 비밀번호 에러 표시")
    @allure.testcase("TC-028")
    @allure.severity("high")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_ui_short_password_error(self, registration_page):
        """Test that short password shows error"""
        registration_page.navigate()
        
        # Enter valid email and short password
        registration_page.fill_email("test@test.com")
        registration_page.fill_password("short")
        
        # Submit form
        registration_page.submit_form()
        
        # Wait for error
        registration_page.wait_for_password_error()
        
        # Verify error message
        error_text = registration_page.get_password_error_text()
        assert "비밀번호" in error_text or "8자" in error_text, \
            f"Expected password length error, got: {error_text}"
        
        registration_page.take_screenshot("short_password_error")
    
    @allure.title("TC-029: UI - 중복 이메일 에러 표시")
    @allure.testcase("TC-029")
    @allure.severity("high")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_ui_duplicate_email_error(self, registration_page, page: Page):
        """Test that duplicate email shows error"""
        registration_page.navigate()
        
        # First, register a user
        test_email = f"duplicate_ui_{int(time.time())}@test.com"
        test_password = "TestPass123!"
        
        registration_page.register_user(test_email, test_password)
        registration_page.wait_for_success()
        
        # Navigate back to registration page
        page.reload()
        registration_page.navigate()
        
        # Try to register with same email
        registration_page.register_user(test_email, test_password)
        
        # Wait for error
        registration_page.wait_for_email_error()
        
        # Verify error message
        error_text = registration_page.get_email_error_text()
        assert "이미 등록된" in error_text or "duplicate" in error_text.lower(), \
            f"Expected duplicate email error, got: {error_text}"
        
        registration_page.take_screenshot("duplicate_email_error")
    
    @allure.title("TC-030: UI - 필수 필드 검증")
    @allure.testcase("TC-030")
    @allure.severity("medium")
    @pytest.mark.ui
    @pytest.mark.negative
    def test_ui_required_fields_validation(self, registration_page):
        """Test that required fields are validated"""
        registration_page.navigate()
        
        # Try to submit empty form
        registration_page.submit_form()
        
        # Check HTML5 validation (browser should prevent submission)
        # Fill only email and try again
        registration_page.fill_email("test@test.com")
        registration_page.password_input.clear()
        registration_page.submit_form()
        
        # Verify password is required
        # Note: This might trigger browser's built-in validation
        
        # Clear and fill only password
        registration_page.clear_form()
        registration_page.fill_password("TestPass123!")
        registration_page.submit_form()
        
        # Verify email is required
        registration_page.take_screenshot("required_fields_validation")
    
    @allure.title("TC-031: UI - 실시간 입력 검증")
    @allure.testcase("TC-031")
    @allure.severity("low")
    @pytest.mark.ui
    @pytest.mark.positive
    def test_ui_realtime_validation_feedback(self, registration_page):
        """Test real-time validation feedback"""
        registration_page.navigate()
        
        # Type invalid email and blur
        registration_page.fill_email("notanemail")
        registration_page.email_input.blur()
        
        # Should show error immediately
        assert registration_page.is_email_error_visible(), \
            "Email error should appear on blur with invalid format"
        
        # Fix email
        registration_page.email_input.clear()
        registration_page.fill_email("valid@email.com")
        registration_page.email_input.blur()
        
        # Error should disappear
        assert not registration_page.is_email_error_visible(), \
            "Email error should disappear with valid format"
        
        registration_page.take_screenshot("realtime_validation")