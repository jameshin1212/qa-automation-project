"""
UI test configuration and fixtures
"""
import pytest
from playwright.sync_api import Page, Browser, Playwright
import allure

@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context configuration"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def registration_page(page: Page):
    """Provide RegistrationPage instance"""
    from pages.registration_page import RegistrationPage
    return RegistrationPage(page)

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Take screenshot on test failure"""
    yield
    
    if request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"failure_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)