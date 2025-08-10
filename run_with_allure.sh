#!/bin/bash

# Allure 리포트와 함께 테스트 실행 스크립트

echo "🧪 WhaTap QA Automation - Allure Report Runner"
echo "=============================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Allure 설치 확인
if ! command -v allure &> /dev/null; then
    echo -e "${RED}❌ Allure가 설치되지 않았습니다.${NC}"
    echo "설치 방법:"
    echo "  Mac: brew install allure"
    echo "  Windows: scoop install allure"
    echo "  Linux: sudo apt-get install allure"
    exit 1
fi

# 이전 결과 정리
if [ -d "allure-results" ]; then
    echo -e "${YELLOW}📁 이전 테스트 결과를 정리합니다...${NC}"
    rm -rf allure-results
fi

# 테스트 유형 선택
echo ""
echo "테스트 유형을 선택하세요:"
echo "1) API 테스트만"
echo "2) UI 테스트만"
echo "3) 전체 테스트"
echo "4) 특정 마커 테스트"
read -p "선택 (1-4): " choice

case $choice in
    1)
        TEST_PATH="tests/api"
        echo -e "${GREEN}✅ API 테스트를 실행합니다${NC}"
        ;;
    2)
        TEST_PATH="tests/ui"
        echo -e "${GREEN}✅ UI 테스트를 실행합니다${NC}"
        ;;
    3)
        TEST_PATH="tests"
        echo -e "${GREEN}✅ 전체 테스트를 실행합니다${NC}"
        ;;
    4)
        echo "마커를 입력하세요 (예: smoke, security, critical):"
        read -p "마커: " marker
        TEST_PATH="-m $marker"
        echo -e "${GREEN}✅ $marker 마커 테스트를 실행합니다${NC}"
        ;;
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac

# 가상환경 활성화
if [ -d "venv" ]; then
    echo -e "${YELLOW}🐍 가상환경을 활성화합니다...${NC}"
    source venv/bin/activate
fi

# Mock 서버 확인
if ! curl -s http://localhost:3000/config > /dev/null; then
    echo -e "${YELLOW}🚀 Mock 서버를 시작합니다...${NC}"
    cd mock_server
    npm start > ../server.log 2>&1 &
    cd ..
    sleep 3
fi

# 테스트 실행
echo ""
echo -e "${GREEN}🧪 테스트를 실행합니다...${NC}"
echo "=============================================="

if [ "$TEST_PATH" = "-m $marker" ]; then
    pytest $TEST_PATH --alluredir=allure-results
else
    pytest $TEST_PATH -v --alluredir=allure-results
fi

TEST_RESULT=$?

# 테스트 결과 확인
echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ 모든 테스트가 성공했습니다!${NC}"
else
    echo -e "${YELLOW}⚠️ 일부 테스트가 실패했습니다${NC}"
fi

# Allure 리포트 생성
echo ""
echo -e "${GREEN}📊 Allure 리포트를 생성합니다...${NC}"
echo "=============================================="

# 리포트 열기 옵션
echo ""
echo "리포트 옵션을 선택하세요:"
echo "1) 브라우저에서 바로 열기 (allure serve)"
echo "2) HTML 파일로 생성 (allure generate)"
echo "3) 둘 다 실행"
echo "4) 건너뛰기"
read -p "선택 (1-4): " report_choice

case $report_choice in
    1)
        echo -e "${GREEN}🌐 브라우저에서 리포트를 엽니다...${NC}"
        allure serve allure-results
        ;;
    2)
        echo -e "${GREEN}📁 HTML 리포트를 생성합니다...${NC}"
        allure generate allure-results -o allure-report --clean
        echo -e "${GREEN}✅ 리포트가 allure-report/ 폴더에 생성되었습니다${NC}"
        echo "열기: open allure-report/index.html"
        ;;
    3)
        echo -e "${GREEN}📁 HTML 리포트를 생성합니다...${NC}"
        allure generate allure-results -o allure-report --clean
        echo -e "${GREEN}🌐 브라우저에서 리포트를 엽니다...${NC}"
        allure serve allure-results
        ;;
    4)
        echo -e "${YELLOW}⏭️ 리포트 생성을 건너뜁니다${NC}"
        ;;
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        ;;
esac

echo ""
echo "=============================================="
echo -e "${GREEN}✅ 완료!${NC}"