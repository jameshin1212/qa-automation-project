#!/bin/bash

# QA Automation Project - Automated Setup Script
# This script automatically sets up the entire test environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_message "$GREEN" "================================================"
print_message "$GREEN" "🚀 QA Automation Project - Automated Setup"
print_message "$GREEN" "================================================"

# Step 1: Check Python version
print_message "$YELLOW" "\n📍 Step 1: Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ -z "$PYTHON_VERSION" ]; then
    print_message "$RED" "❌ Python 3 is not installed!"
    print_message "$YELLOW" "Please install Python 3.8 or higher"
    exit 1
fi

print_message "$GREEN" "✅ Found Python $PYTHON_VERSION"

if [ "$PYTHON_MINOR" -ge 13 ]; then
    print_message "$YELLOW" "⚠️  Python 3.13+ detected. Some packages may have compatibility issues."
    REQUIREMENTS_FILE="requirements-minimal.txt"
    
    # Create minimal requirements file if it doesn't exist
    if [ ! -f "requirements-minimal.txt" ]; then
        print_message "$YELLOW" "Creating minimal requirements file..."
        cat > requirements-minimal.txt << 'EOF'
# Core testing frameworks
pytest==7.4.3
pytest-html==4.1.1
pytest-xdist==3.5.0
pytest-rerunfailures==12.0

# API testing
requests==2.31.0
jsonschema==4.20.0

# UI testing (may need special installation)
playwright==1.40.0
pytest-playwright==0.4.3

# Reporting
allure-pytest==2.13.2
pytest-json-report==1.5.0

# Data handling
faker==20.1.0
python-dotenv==1.0.0

# Excel handling (without pandas)
openpyxl==3.1.2

# Utilities
colorlog==6.8.0
python-dateutil==2.8.2
EOF
    fi
elif [ "$PYTHON_MINOR" -ge 8 ] && [ "$PYTHON_MINOR" -le 12 ]; then
    print_message "$GREEN" "✅ Python version is compatible"
    REQUIREMENTS_FILE="requirements.txt"
else
    print_message "$RED" "❌ Python 3.$PYTHON_MINOR is too old. Minimum required: Python 3.8"
    exit 1
fi

# Step 2: Check Node.js and npm
print_message "$YELLOW" "\n📍 Step 2: Checking Node.js and npm..."
if ! command -v node &> /dev/null; then
    print_message "$RED" "❌ Node.js is not installed!"
    print_message "$YELLOW" "Please install Node.js from https://nodejs.org/"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_message "$RED" "❌ npm is not installed!"
    exit 1
fi

NODE_VERSION=$(node --version)
NPM_VERSION=$(npm --version)
print_message "$GREEN" "✅ Found Node.js $NODE_VERSION and npm $NPM_VERSION"

# Step 3: Create Python virtual environment
print_message "$YELLOW" "\n📍 Step 3: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_message "$GREEN" "✅ Created virtual environment"
else
    print_message "$GREEN" "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_message "$GREEN" "✅ Activated virtual environment"

# Step 4: Install Python dependencies
print_message "$YELLOW" "\n📍 Step 4: Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r $REQUIREMENTS_FILE

if [ $? -eq 0 ]; then
    print_message "$GREEN" "✅ Python dependencies installed successfully"
else
    print_message "$YELLOW" "⚠️  Some packages failed to install. Trying alternative approach..."
    
    # Try installing packages one by one
    while IFS= read -r line; do
        if [[ ! "$line" =~ ^# ]] && [[ ! -z "$line" ]]; then
            package=$(echo $line | cut -d= -f1)
            pip install $line 2>/dev/null || print_message "$YELLOW" "   Skipped: $package"
        fi
    done < $REQUIREMENTS_FILE
fi

# Step 5: Install Playwright browsers
print_message "$YELLOW" "\n📍 Step 5: Installing Playwright browsers..."
if command -v playwright &> /dev/null; then
    playwright install webkit
    print_message "$GREEN" "✅ Playwright browsers installed"
else
    print_message "$YELLOW" "⚠️  Playwright not found. You may need to install it manually."
fi

# Step 6: Install Mock Server dependencies
print_message "$YELLOW" "\n📍 Step 6: Installing Mock Server dependencies..."
cd mock_server
if [ ! -d "node_modules" ]; then
    npm install
    print_message "$GREEN" "✅ Mock server dependencies installed"
else
    print_message "$GREEN" "✅ Mock server dependencies already installed"
fi
cd ..

# Step 7: Check port availability
print_message "$YELLOW" "\n📍 Step 7: Checking port availability..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_message "$YELLOW" "⚠️  Port 3000 is in use. Mock server will use an alternative port."
else
    print_message "$GREEN" "✅ Port 3000 is available"
fi

# Step 8: Create necessary directories
print_message "$YELLOW" "\n📍 Step 8: Creating necessary directories..."
mkdir -p reports allure-results allure-report
print_message "$GREEN" "✅ Created report directories"

# Step 9: Verify setup
print_message "$YELLOW" "\n📍 Step 9: Verifying setup..."
python3 setup_validator.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_message "$GREEN" "✅ Environment validation passed"
else
    print_message "$YELLOW" "⚠️  Some validation checks failed. Run 'python3 setup_validator.py' for details."
fi

# Final message
print_message "$GREEN" "\n================================================"
print_message "$GREEN" "🎉 Setup Complete!"
print_message "$GREEN" "================================================"
print_message "$GREEN" "\n📝 Next Steps:"
print_message "$GREEN" "1. Start mock server: cd mock_server && npm start"
print_message "$GREEN" "2. Run tests: pytest -v"
print_message "$GREEN" "3. Or use the automated script: ./run_tests.sh"
print_message "$GREEN" "\n💡 Tip: Run 'python3 setup_validator.py' to check environment status"
print_message "$GREEN" "================================================\n"

# Create run_tests.sh if it doesn't exist
if [ ! -f "run_tests.sh" ]; then
    print_message "$YELLOW" "Creating run_tests.sh script..."
    cat > run_tests.sh << 'EOF'
#!/bin/bash

# QA Automation - Test Runner Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🧪 Starting QA Automation Tests${NC}"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${RED}❌ Virtual environment not found. Run ./setup.sh first${NC}"
    exit 1
fi

# Start mock server in background
echo -e "${YELLOW}Starting mock server...${NC}"
cd mock_server
npm start > ../server.log 2>&1 &
SERVER_PID=$!
cd ..

# Wait for server to be ready
echo -e "${YELLOW}Waiting for mock server to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:3000/config > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Mock server is ready${NC}"
        break
    fi
    sleep 1
done

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
pytest -v --tb=short

# Kill mock server
echo -e "${YELLOW}Stopping mock server...${NC}"
kill $SERVER_PID 2>/dev/null

echo -e "${GREEN}✅ Tests complete${NC}"
EOF
    chmod +x run_tests.sh
    print_message "$GREEN" "✅ Created run_tests.sh script"
fi