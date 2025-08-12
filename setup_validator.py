#!/usr/bin/env python3
"""
Environment Setup Validator for QA Automation Project
Checks system requirements and provides guidance for successful test execution
"""

import sys
import subprocess
import json
import os
from pathlib import Path
import platform
import shutil

class SetupValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_messages = []
        self.python_version = sys.version_info
        self.project_root = Path(__file__).parent
        
    def check_python_version(self):
        """Check Python version compatibility"""
        print("🔍 Checking Python version...")
        version_str = f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 8):
            self.errors.append(f"❌ Python {version_str} is too old. Minimum required: Python 3.8")
            return False
        
        if self.python_version.major == 3 and self.python_version.minor == 13:
            self.warnings.append(f"⚠️  Python {version_str} has compatibility issues with some dependencies")
            self.warnings.append("   Recommended: Python 3.12 for full compatibility")
            return True
            
        if self.python_version.major == 3 and 8 <= self.python_version.minor <= 12:
            self.success_messages.append(f"✅ Python {version_str} is compatible")
            return True
            
        self.warnings.append(f"⚠️  Python {version_str} has not been tested")
        return True
    
    def check_node_installation(self):
        """Check Node.js installation and version"""
        print("🔍 Checking Node.js installation...")
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.success_messages.append(f"✅ Node.js {version} is installed")
                
                # Check version requirement (Node 14+)
                major_version = int(version.split('.')[0].replace('v', ''))
                if major_version < 14:
                    self.warnings.append(f"⚠️  Node.js {version} is old. Recommended: v14 or higher")
                return True
            else:
                self.errors.append("❌ Node.js is not installed")
                return False
        except FileNotFoundError:
            self.errors.append("❌ Node.js is not installed")
            self.errors.append("   Install from: https://nodejs.org/")
            return False
        except Exception as e:
            self.warnings.append(f"⚠️  Could not verify Node.js: {e}")
            return False
    
    def check_npm_installation(self):
        """Check npm installation"""
        print("🔍 Checking npm installation...")
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.success_messages.append(f"✅ npm {version} is installed")
                return True
            else:
                self.errors.append("❌ npm is not installed")
                return False
        except FileNotFoundError:
            self.errors.append("❌ npm is not installed")
            return False
        except Exception as e:
            self.warnings.append(f"⚠️  Could not verify npm: {e}")
            return False
    
    def check_port_availability(self, port=3000):
        """Check if port 3000 is available"""
        print(f"🔍 Checking port {port} availability...")
        import socket
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            self.warnings.append(f"⚠️  Port {port} is already in use")
            self.warnings.append(f"   To free the port, run: kill -9 $(lsof -t -i:{port})")
            return False
        else:
            self.success_messages.append(f"✅ Port {port} is available")
            return True
    
    def check_venv_setup(self):
        """Check if virtual environment is properly set up"""
        print("🔍 Checking virtual environment...")
        venv_path = self.project_root / "venv"
        
        if venv_path.exists():
            if sys.prefix == sys.base_prefix:
                self.warnings.append("⚠️  Virtual environment exists but is not activated")
                self.warnings.append("   Activate with: source venv/bin/activate")
                return False
            else:
                self.success_messages.append("✅ Virtual environment is active")
                return True
        else:
            self.warnings.append("⚠️  Virtual environment not found")
            self.warnings.append(f"   Create with: python3 -m venv venv")
            return False
    
    def check_required_files(self):
        """Check if all required files exist"""
        print("🔍 Checking required files...")
        required_files = [
            "requirements.txt",
            "pytest.ini",
            "conftest.py",
            "mock_server/package.json",
            "mock_server/server.js",
            "mock_server/db-backup.json"
        ]
        
        all_exist = True
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.errors.append(f"❌ Missing required file: {file_path}")
                all_exist = False
        
        if all_exist:
            self.success_messages.append("✅ All required files are present")
        
        return all_exist
    
    def check_mock_server_dependencies(self):
        """Check if mock server dependencies are installed"""
        print("🔍 Checking mock server dependencies...")
        node_modules = self.project_root / "mock_server" / "node_modules"
        
        if node_modules.exists():
            self.success_messages.append("✅ Mock server dependencies are installed")
            return True
        else:
            self.warnings.append("⚠️  Mock server dependencies not installed")
            self.warnings.append("   Install with: cd mock_server && npm install")
            return False
    
    def check_python_packages(self):
        """Check if Python packages can be installed"""
        print("🔍 Checking Python package compatibility...")
        
        # Check for problematic packages based on Python version
        if self.python_version.minor == 13:
            self.warnings.append("⚠️  Python 3.13 has known issues with:")
            self.warnings.append("   - pandas (not yet compatible)")
            self.warnings.append("   - greenlet (playwright dependency)")
            self.warnings.append("   Use requirements-minimal.txt for basic functionality")
            return True
        
        self.success_messages.append("✅ Python package compatibility looks good")
        return True
    
    def suggest_quick_fix(self):
        """Provide quick fix suggestions based on detected issues"""
        print("\n" + "="*60)
        print("📋 QUICK FIX SUGGESTIONS")
        print("="*60)
        
        if self.errors:
            print("\n🚨 Critical Issues (must fix):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  Warnings (recommended to fix):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        # Provide setup script
        if self.errors or self.warnings:
            print("\n🔧 Quick Setup Commands:")
            print("```bash")
            
            if not self.check_venv_setup():
                print(f"# Create and activate virtual environment")
                print(f"python3.12 -m venv venv")
                print(f"source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
                print()
            
            print(f"# Install Python dependencies")
            if self.python_version.minor == 13:
                print(f"pip install -r requirements-minimal.txt")
            else:
                print(f"pip install -r requirements.txt")
            print()
            
            if not (self.project_root / "mock_server" / "node_modules").exists():
                print(f"# Install mock server dependencies")
                print(f"cd mock_server && npm install && cd ..")
            print()
            
            print(f"# Install Playwright browsers")
            print(f"playwright install webkit")
            print("```")
    
    def generate_report(self):
        """Generate environment validation report"""
        print("\n" + "="*60)
        print("🔬 ENVIRONMENT VALIDATION REPORT")
        print("="*60)
        
        total_checks = len(self.success_messages) + len(self.warnings) + len(self.errors)
        success_rate = (len(self.success_messages) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 Summary:")
        print(f"  ✅ Passed: {len(self.success_messages)}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        print(f"  ❌ Failed: {len(self.errors)}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        if self.success_messages:
            print(f"\n✅ Successful Checks:")
            for msg in self.success_messages:
                print(f"  {msg}")
        
        print("\n" + "="*60)
        
        # Determine overall status
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print("🎉 RESULT: Environment is perfectly configured!")
                print("You can proceed with running tests.")
            else:
                print("✅ RESULT: Environment is usable with minor issues.")
                print("Tests should work but consider fixing warnings.")
        else:
            print("❌ RESULT: Environment has critical issues.")
            print("Please fix the errors before running tests.")
        
        print("="*60)
        
        return len(self.errors) == 0
    
    def run_validation(self):
        """Run all validation checks"""
        print("="*60)
        print("🚀 QA Automation Project - Environment Validator")
        print("="*60)
        print(f"📍 Project Directory: {self.project_root}")
        print(f"🐍 Python Executable: {sys.executable}")
        print(f"💻 Platform: {platform.system()} {platform.release()}")
        print("="*60 + "\n")
        
        # Run all checks
        self.check_python_version()
        self.check_node_installation()
        self.check_npm_installation()
        self.check_port_availability()
        self.check_venv_setup()
        self.check_required_files()
        self.check_mock_server_dependencies()
        self.check_python_packages()
        
        # Generate report
        success = self.generate_report()
        
        # Provide quick fix suggestions
        self.suggest_quick_fix()
        
        return success

if __name__ == "__main__":
    validator = SetupValidator()
    success = validator.run_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)