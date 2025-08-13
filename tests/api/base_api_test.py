"""
Base class for API tests
"""
import pytest
import json
import allure
from typing import Dict, Any, Optional
from datetime import datetime

class BaseAPITest:
    """Base class providing common functionality for API tests"""
    
    @pytest.fixture(autouse=True)
    def setup_api_test(self, api_client, api_endpoints, test_data):
        """Setup for each API test"""
        self.client = api_client
        self.endpoints = api_endpoints
        self.test_data = test_data
        self.created_users = []
        
        yield
        
        # Cleanup created users
        for user_id in self.created_users:
            try:
                self.client.delete(f"{self.endpoints['users']}/{user_id}")
            except:
                pass
    
    def register_user(self, email: str, password: str, 
                     expected_status: int = 200) -> Dict[str, Any]:
        """
        Helper method to register a user
        
        Args:
            email: User email
            password: User password
            expected_status: Expected HTTP status code
            
        Returns:
            Response data as dictionary
        """
        payload = {
            "email": email,
            "password": password,
            "created_at": datetime.now().isoformat()
        }
        
        with allure.step(f"Register user with email: {email}"):
            response = self.client.post(
                self.endpoints["register"],
                json=payload
            )
            
            allure.attach(
                json.dumps(payload, indent=2),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )
            
            allure.attach(
                json.dumps(response.json() if response.text else {}, indent=2),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}"
            
            if response.status_code == 200:
                user_data = response.json()
                if "id" in user_data:
                    self.created_users.append(user_data["id"])
            
            return response.json() if response.text else {}
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email
        
        Args:
            email: User email to search
            
        Returns:
            User data if found, None otherwise
        """
        with allure.step(f"Get user by email: {email}"):
            response = self.client.get(
                self.endpoints["users"],
                params={"email": email}
            )
            
            if response.status_code == 200:
                users = response.json()
                return users[0] if users else None
            return None
    
    def check_duplicate_email(self, email: str) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            
        Returns:
            True if email exists, False otherwise
        """
        user = self.get_user_by_email(email)
        return user is not None
    
    def validate_password_complexity(self, password: str) -> Dict[str, bool]:
        """
        Validate password complexity requirements
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results
        """
        validations = {
            "min_length": len(password) >= 8,
            "has_lowercase": any(c.islower() for c in password),
            "has_uppercase": any(c.isupper() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in "@$!%*?&" for c in password)
        }
        
        validations["is_valid"] = all(validations.values())
        return validations
    
    def validate_email_format(self, email: str) -> bool:
        """
        Basic email format validation
        
        Args:
            email: Email to validate
            
        Returns:
            True if valid email format, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    def validate_timestamp(self, timestamp: str) -> bool:
        """
        Validate ISO 8601 timestamp format
        
        Args:
            timestamp: Timestamp string to validate
            
        Returns:
            True if valid ISO timestamp, False otherwise
        """
        try:
            from datetime import datetime
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except:
            return False