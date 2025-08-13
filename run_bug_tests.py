#!/usr/bin/env python3
"""
Direct bug detection test runner for Docker environment
Bypasses conftest.py server startup for Docker container
"""
import subprocess
import sys
import os

# Set environment to skip server startup in conftest
os.environ['SKIP_SERVER_STARTUP'] = 'true'
# Force API_BASE_URL for Docker environment
if 'DOCKER_ENV' in os.environ:
    os.environ['API_BASE_URL'] = 'http://qa-server:3000'
else:
    os.environ['API_BASE_URL'] = os.getenv('API_BASE_URL', 'http://localhost:3000')

print(f"Using API_BASE_URL: {os.environ['API_BASE_URL']}")

# Run bug detection tests directly
result = subprocess.run([
    'pytest',
    'tests/api/test_bug_detection.py',
    '-v',
    '--alluredir=allure-results',
    '--tb=short'
], capture_output=False, text=True)

sys.exit(result.returncode)