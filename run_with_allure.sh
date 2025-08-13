#!/bin/bash

# 색상 설정
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting QA Tests with Allure Report...${NC}"

# 이전 결과 정리
echo -e "${YELLOW}Cleaning previous results...${NC}"
rm -rf ./allure-results
rm -rf ./allure-report

# Mock Server 시작 (백그라운드)
echo -e "${YELLOW}Starting Mock Server...${NC}"
cd mock_server
npm start &
MOCK_PID=$!
cd ..

# Mock Server가 준비될 때까지 대기
echo -e "${YELLOW}Waiting for Mock Server to be ready...${NC}"
for i in {1..30}; do
    if curl -f http://localhost:3000/config > /dev/null 2>&1; then
        echo -e "${GREEN}Mock Server is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Mock Server failed to start${NC}"
        kill $MOCK_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

# 테스트 실행
echo -e "${GREEN}Running Tests...${NC}"
python -m pytest tests/ -v --alluredir=./allure-results

# 테스트 결과 저장
TEST_RESULT=$?

# Allure 리포트 생성
echo -e "${YELLOW}Generating Allure Report...${NC}"
allure generate ./allure-results --clean -o ./allure-report

# Allure 서버 시작
echo -e "${GREEN}Starting Allure Server...${NC}"
echo -e "${GREEN}Report will be available at: http://localhost:5050${NC}"
allure serve ./allure-results -p 5050

# Cleanup
kill $MOCK_PID 2>/dev/null

# 테스트 결과 반환
exit $TEST_RESULT