#!/bin/bash

# Docker를 사용한 WhaTap QA 자동화 테스트 실행 스크립트

echo "🐳 WhaTap QA Automation - Docker Runner"
echo "=========================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Docker 설치 확인
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker가 설치되지 않았습니다.${NC}"
    echo "설치 방법: https://docs.docker.com/get-docker/"
    exit 1
fi

# Docker Compose 설치 확인
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose가 설치되지 않았습니다.${NC}"
    echo "설치 방법: https://docs.docker.com/compose/install/"
    exit 1
fi

# 실행 옵션 선택
echo ""
echo "실행 옵션을 선택하세요:"
echo "1) 🚀 빠른 테스트 (API 테스트만)"
echo "2) 🧪 전체 테스트 (API + UI)"
echo "3) 📊 테스트 + Allure Report 서버"
echo "4) 🧹 컨테이너 정리"
echo "5) 🔄 재빌드 후 테스트"
read -p "선택 (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}✅ API 테스트를 Docker로 실행합니다${NC}"
        docker-compose up mock-server -d
        sleep 5
        docker-compose run --rm test-runner pytest tests/api -v --alluredir=allure-results
        ;;
    2)
        echo -e "${GREEN}✅ 전체 테스트를 Docker로 실행합니다${NC}"
        docker-compose up mock-server -d
        sleep 5
        docker-compose run --rm test-runner
        ;;
    3)
        echo -e "${GREEN}✅ 테스트 + Allure Report 서버를 실행합니다${NC}"
        docker-compose --profile with-report up
        echo -e "${BLUE}📊 Allure Report: http://localhost:5050${NC}"
        ;;
    4)
        echo -e "${YELLOW}🧹 Docker 컨테이너를 정리합니다${NC}"
        docker-compose down -v
        docker system prune -f
        echo -e "${GREEN}✅ 정리 완료${NC}"
        ;;
    5)
        echo -e "${YELLOW}🔄 이미지를 재빌드하고 테스트를 실행합니다${NC}"
        docker-compose build --no-cache
        docker-compose up mock-server -d
        sleep 5
        docker-compose run --rm test-runner
        ;;
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac

# 테스트 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 테스트가 완료되었습니다!${NC}"
    
    # Allure Report 생성 옵션
    if [ "$choice" != "4" ]; then
        echo ""
        echo "Allure Report를 생성하시겠습니까? (y/n)"
        read -p "선택: " report_choice
        
        if [ "$report_choice" = "y" ] || [ "$report_choice" = "Y" ]; then
            echo -e "${BLUE}📊 Allure Report를 생성합니다...${NC}"
            docker-compose run --rm test-runner allure generate allure-results -o allure-report --clean
            echo -e "${GREEN}✅ 리포트가 ./allure-report에 생성되었습니다${NC}"
            echo "열기: open allure-report/index.html"
        fi
    fi
else
    echo -e "${RED}❌ 테스트 실행 중 오류가 발생했습니다${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ 완료!${NC}"