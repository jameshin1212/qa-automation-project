#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    QA Automation Test Runner${NC}"
echo -e "${GREEN}========================================${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null
}

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js found${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies if needed
if ! pip show pytest > /dev/null 2>&1; then
    echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    playwright install chromium
fi

# Check if mock server dependencies are installed
if [ ! -d "mock_server/node_modules" ]; then
    echo -e "\n${YELLOW}Installing Mock server dependencies...${NC}"
    cd mock_server
    npm install
    cd ..
fi

# Start mock server if not running
if ! port_in_use 3000; then
    echo -e "\n${YELLOW}Starting Mock server...${NC}"
    cd mock_server
    npm start > /dev/null 2>&1 &
    SERVER_PID=$!
    cd ..
    
    # Wait for server to start
    echo -n "Waiting for server to start"
    for i in {1..10}; do
        if curl -s http://localhost:3000/config > /dev/null; then
            echo -e "\n${GREEN}✅ Mock server started${NC}"
            break
        fi
        echo -n "."
        sleep 1
    done
else
    echo -e "\n${GREEN}✅ Mock server already running${NC}"
fi

# Menu for test selection
echo -e "\n${YELLOW}Select test suite to run:${NC}"
echo "1) All tests"
echo "2) API tests only"
echo "3) UI tests only"
echo "4) Smoke tests"
echo "5) Security tests"
echo "6) Generate Allure Report"
echo "7) Exit"

read -p "Enter your choice [1-7]: " choice

case $choice in
    1)
        echo -e "\n${YELLOW}Running all tests...${NC}"
        pytest -v --alluredir=allure-results
        ;;
    2)
        echo -e "\n${YELLOW}Running API tests...${NC}"
        pytest tests/api -v --alluredir=allure-results
        ;;
    3)
        echo -e "\n${YELLOW}Running UI tests...${NC}"
        pytest tests/ui -v --alluredir=allure-results
        ;;
    4)
        echo -e "\n${YELLOW}Running smoke tests...${NC}"
        pytest -m smoke -v --alluredir=allure-results
        ;;
    5)
        echo -e "\n${YELLOW}Running security tests...${NC}"
        pytest -m security -v --alluredir=allure-results
        ;;
    6)
        echo -e "\n${YELLOW}Generating Allure Report...${NC}"
        if command_exists allure; then
            allure serve allure-results
        else
            echo -e "${RED}Allure is not installed. Install with: npm install -g allure-commandline${NC}"
        fi
        ;;
    7)
        echo -e "\n${GREEN}Exiting...${NC}"
        ;;
    *)
        echo -e "\n${RED}Invalid choice${NC}"
        ;;
esac

# Cleanup
if [ ! -z "$SERVER_PID" ]; then
    echo -e "\n${YELLOW}Stopping Mock server...${NC}"
    kill $SERVER_PID 2>/dev/null
fi

echo -e "\n${GREEN}Test execution completed!${NC}"