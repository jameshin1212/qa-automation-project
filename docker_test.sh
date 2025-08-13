#!/bin/bash

# 색상 설정
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting QA Automation Test Environment...${NC}"

# Mock Server 시작
echo -e "${YELLOW}Starting Mock Server...${NC}"
cd /app/mock_server
npm start &
MOCK_PID=$!

# Mock Server가 준비될 때까지 대기
echo -e "${YELLOW}Waiting for Mock Server to be ready...${NC}"
for i in {1..30}; do
    if curl -f http://localhost:3000/config > /dev/null 2>&1; then
        echo -e "${GREEN}Mock Server is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Mock Server failed to start${NC}"
        exit 1
    fi
    sleep 1
done

cd /app

# 테스트 실행 옵션 처리
if [ "$1" = "test" ]; then
    echo -e "${GREEN}Running Tests...${NC}"
    python -m pytest tests/ -v --alluredir=./allure-results
elif [ "$1" = "allure" ]; then
    echo -e "${GREEN}Running Tests with Allure Report...${NC}"
    # 이전 결과 정리
    rm -rf ./allure-results
    rm -rf ./allure-report
    
    # 테스트 실행
    python -m pytest tests/ -v --alluredir=./allure-results
    
    # Allure 리포트 생성
    echo -e "${YELLOW}Generating Allure Report...${NC}"
    allure generate ./allure-results --clean -o ./allure-report
    
    # Allure 서버 시작
    echo -e "${GREEN}Starting Allure Server on port 5050...${NC}"
    allure serve ./allure-results -p 5050 &
    ALLURE_PID=$!
    
    echo -e "${GREEN}Allure Report is available at http://localhost:5050${NC}"
    
    # Keep container running
    tail -f /dev/null
else
    echo -e "${GREEN}Container is ready. Mock Server running on port 3000${NC}"
    echo -e "${YELLOW}Available commands:${NC}"
    echo "  docker exec -it <container_name> /docker_test.sh test    # Run tests"
    echo "  docker exec -it <container_name> /docker_test.sh allure  # Run tests with Allure report"
    echo "  docker exec -it <container_name> bash                    # Interactive shell"
    
    # Keep container running
    tail -f /dev/null
fi

# Cleanup on exit
trap "kill $MOCK_PID $ALLURE_PID 2>/dev/null; exit" SIGINT SIGTERM