"""
Page Object Model for Registration Page
"""
from playwright.sync_api import Page, expect

# Allure를 옵셔널하게 import
try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    # allure가 없을 때를 위한 더미 데코레이터
    class allure:
        @staticmethod
        def step(name):
            return lambda x: x

class RegistrationPage:
    """Page Object for the registration form"""
    
    def __init__(self, page: Page):
        self.page = page
        import os
        # Docker 환경에서는 qa-server 사용
        base_url = os.getenv("API_BASE_URL", "http://localhost:3000")
        if "qa-server" in base_url:
            self.url = "http://qa-server:3000/index.html"
        else:
            self.url = "http://localhost:3000/index.html"
        
        # Locators
        self.email_input = page.locator('[data-testid="email-input"]')
        self.password_input = page.locator('[data-testid="password-input"]')
        self.submit_button = page.locator('[data-testid="submit-button"]')
        
        # Error message locators
        self.email_error = page.locator('#emailError')
        self.password_error = page.locator('#passwordError')
        self.general_error = page.locator('#generalError')
        
        # Success message
        self.success_message = page.locator('#successMessage')
        
        # Form
        self.registration_form = page.locator('#registrationForm')
    
    @allure.step("Navigate to registration page")
    def navigate(self):
        """Navigate to the registration page"""
        self.page.goto(self.url)
        expect(self.registration_form).to_be_visible()
    
    @allure.step("Fill email: {email}")
    def fill_email(self, email: str):
        """Fill in the email field"""
        self.email_input.fill(email)
    
    @allure.step("Fill password")
    def fill_password(self, password: str):
        """Fill in the password field"""
        self.password_input.fill(password)
    
    @allure.step("Submit registration form")
    def submit_form(self):
        """Submit the registration form"""
        self.submit_button.click()
    
    @allure.step("Register user with email: {email}")
    def register_user(self, email: str, password: str):
        """Complete registration process"""
        self.fill_email(email)
        self.fill_password(password)
        self.submit_form()
    
    def is_success_message_visible(self) -> bool:
        """Check if success message is visible"""
        return self.success_message.is_visible()
    
    def is_email_error_visible(self) -> bool:
        """Check if email error is visible"""
        return self.email_error.is_visible()
    
    def is_password_error_visible(self) -> bool:
        """Check if password error is visible"""
        return self.password_error.is_visible()
    
    def is_general_error_visible(self) -> bool:
        """Check if general error is visible"""
        return self.general_error.is_visible()
    
    def get_email_error_text(self) -> str:
        """Get email error message text"""
        if self.is_email_error_visible():
            return self.email_error.text_content()
        return ""
    
    def get_password_error_text(self) -> str:
        """Get password error message text"""
        if self.is_password_error_visible():
            return self.password_error.text_content()
        return ""
    
    def get_general_error_text(self) -> str:
        """Get general error message text"""
        if self.is_general_error_visible():
            return self.general_error.text_content()
        return ""
    
    def wait_for_success(self, timeout: int = 5000):
        """Wait for success message to appear"""
        expect(self.success_message).to_be_visible(timeout=timeout)
    
    def wait_for_email_error(self, timeout: int = 3000):
        """Wait for email error to appear"""
        expect(self.email_error).to_be_visible(timeout=timeout)
    
    def wait_for_password_error(self, timeout: int = 3000):
        """Wait for password error to appear"""
        expect(self.password_error).to_be_visible(timeout=timeout)
    
    def clear_form(self):
        """Clear all form fields"""
        self.email_input.clear()
        self.password_input.clear()
    
    def is_submit_button_enabled(self) -> bool:
        """Check if submit button is enabled"""
        return self.submit_button.is_enabled()
    
    def take_screenshot(self, name: str):
        """Take a screenshot of the current page"""
        screenshot = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )