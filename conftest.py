"""
Global pytest configuration and fixtures
"""
import pytest
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
import requests
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).parent
MOCK_SERVER_DIR = PROJECT_ROOT / "mock_server"
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"
REPORTS_DIR = PROJECT_ROOT / "reports"

# API configuration
# Docker 환경에서는 qa-server:3000 사용
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
if "qa-server" in API_BASE_URL:
    # Docker 환경: 명시적으로 qa-server 사용
    API_BASE_URL = "http://qa-server:3000"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before all tests"""
    print("\n=== Setting up test environment ===")
    
    # Create reports directory if not exists
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Check if we're in Docker environment or server is already running
    server_already_running = False
    try:
        response = requests.get(f"{API_BASE_URL}/config", timeout=1)
        if response.status_code == 200:
            server_already_running = True
            print("Mock Server is already running!")
    except:
        pass
    
    if server_already_running:
        # Server is already running (Docker or manually started)
        print("Using existing Mock Server")
        yield
        print("\n=== Test environment cleanup (existing server) ===")
    else:
        # Start JSON Server locally
        print("Starting JSON Server...")
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=MOCK_SERVER_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                # Try /config first, fallback to /users endpoint
                try:
                    response = requests.get(f"{API_BASE_URL}/config")
                    if response.status_code == 200:
                        print("JSON Server is ready! (config endpoint)")
                        break
                except:
                    pass
                
                # Fallback to /users endpoint
                response = requests.get(f"{API_BASE_URL}/users")
                if response.status_code == 200:
                    print("JSON Server is ready! (users endpoint)")
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        else:
            process.terminate()
            raise RuntimeError("Failed to start JSON Server")
        
        yield
        
        # Cleanup
        print("\n=== Cleaning up test environment ===")
        process.terminate()
        process.wait()

@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    # Always use paths relative to project structure
    backup_path = MOCK_SERVER_DIR / "db-backup.json"
    db_path = MOCK_SERVER_DIR / "db.json"
    
    # In Docker, these paths are also correct since we mount the entire app
    shutil.copy(backup_path, db_path)
    time.sleep(0.5)  # Wait for JSON Server to reload
    
    yield
    
    # Optional: Save test data for debugging failed tests
    if hasattr(pytest, "test_failed") and pytest.test_failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_file = REPORTS_DIR / f"debug_db_{timestamp}.json"
        shutil.copy(db_path, debug_file)

@pytest.fixture
def api_client():
    """Provide configured requests session for API testing"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    return session

@pytest.fixture
def test_data():
    """Load test data fixtures"""
    fixtures = {}
    fixtures_path = FIXTURES_DIR / "test_data.json"
    
    if fixtures_path.exists():
        with open(fixtures_path, 'r', encoding='utf-8') as f:
            fixtures = json.load(f)
    
    return fixtures

@pytest.fixture
def api_endpoints():
    """API endpoints configuration"""
    return {
        "register": f"{API_BASE_URL}/api/register",
        "users": f"{API_BASE_URL}/users",
        "config": f"{API_BASE_URL}/config",
    }

# Pytest hooks for better reporting
def pytest_configure(config):
    """Configure pytest with custom settings"""
    config._metadata = {
        "Project": "QA Automation - User Registration",
        "Test Framework": "pytest",
        "API Framework": "requests",
        "UI Framework": "Playwright"
    }

# def pytest_html_report_title(report):
#     """Set HTML report title"""
#     report.title = "QA Automation Test Report"

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Mark test as failed for fixture cleanup"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        pytest.test_failed = True
    else:
        pytest.test_failed = False