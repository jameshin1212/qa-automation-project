#!/bin/bash

# Docker Allure Report 실행 스크립트

echo "🐳 WhaTap QA - Docker Allure Report"
echo "===================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 실행 옵션 선택
echo ""
echo "옵션을 선택하세요:"
echo "1) 🧪 테스트 실행 + Allure 리포트 생성"
echo "2) 📊 기존 결과로 Allure 리포트 생성"
echo "3) 🌐 Allure 서버 실행 (포트 5050)"
echo "4) 🔄 전체 실행 (테스트 + 리포트 + 서버)"
echo "5) 🧹 정리 (컨테이너 및 결과 삭제)"
read -p "선택 (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}✅ 테스트 실행 및 Allure 리포트 생성${NC}"
        
        # Mock Server 시작
        docker-compose up -d mock-server
        sleep 5
        
        # 테스트 실행 with Allure
        echo -e "${YELLOW}🧪 테스트 실행 중...${NC}"
        docker-compose run --rm test-runner bash -c "
            pytest tests/api tests/ui --alluredir=/app/allure-results -v
        "
        
        # Allure Report 생성
        echo -e "${YELLOW}📊 Allure 리포트 생성 중...${NC}"
        docker-compose run --rm test-runner bash -c "
            allure generate /app/allure-results -o /app/allure-report --clean
        "
        
        echo -e "${GREEN}✅ 리포트가 생성되었습니다: ./allure-report/index.html${NC}"
        echo -e "${BLUE}열기: open allure-report/index.html${NC}"
        ;;
        
    2)
        echo -e "${GREEN}✅ 기존 결과로 Allure 리포트 생성${NC}"
        
        # Allure Report 생성
        docker-compose run --rm test-runner bash -c "
            allure generate /app/allure-results -o /app/allure-report --clean
        "
        
        echo -e "${GREEN}✅ 리포트가 생성되었습니다: ./allure-report/index.html${NC}"
        echo -e "${BLUE}열기: open allure-report/index.html${NC}"
        ;;
        
    3)
        echo -e "${GREEN}✅ Allure 서버 실행${NC}"
        
        # Allure 서버 실행
        echo -e "${YELLOW}🌐 Allure 서버를 시작합니다 (포트 5050)...${NC}"
        echo -e "${BLUE}브라우저에서 열기: http://localhost:5050${NC}"
        echo -e "${YELLOW}종료: Ctrl+C${NC}"
        
        docker-compose run --rm -p 5050:5050 test-runner bash -c "
            allure serve /app/allure-results -p 5050 --host 0.0.0.0
        "
        ;;
        
    4)
        echo -e "${GREEN}✅ 전체 실행 (테스트 + 리포트 + 서버)${NC}"
        
        # Mock Server 시작
        docker-compose up -d mock-server
        sleep 5
        
        # 테스트 실행
        echo -e "${YELLOW}🧪 테스트 실행 중...${NC}"
        docker-compose run --rm test-runner bash -c "
            pytest tests/api tests/ui --alluredir=/app/allure-results -v
        "
        
        # Allure Report 생성
        echo -e "${YELLOW}📊 Allure 리포트 생성 중...${NC}"
        docker-compose run --rm test-runner bash -c "
            allure generate /app/allure-results -o /app/allure-report --clean
        "
        
        # Allure 서버 실행
        echo -e "${GREEN}✅ 리포트가 생성되었습니다${NC}"
        echo -e "${YELLOW}🌐 Allure 서버를 시작합니다...${NC}"
        echo -e "${BLUE}브라우저에서 열기: http://localhost:5050${NC}"
        echo -e "${YELLOW}종료: Ctrl+C${NC}"
        
        docker-compose run --rm -p 5050:5050 test-runner bash -c "
            allure serve /app/allure-results -p 5050 --host 0.0.0.0
        "
        ;;
        
    5)
        echo -e "${YELLOW}🧹 정리 중...${NC}"
        
        # 컨테이너 정리
        docker-compose down -v
        
        # 결과 파일 정리 확인
        echo ""
        echo "Allure 결과 파일도 삭제하시겠습니까? (y/n)"
        read -p "선택: " clean_choice
        
        if [ "$clean_choice" = "y" ] || [ "$clean_choice" = "Y" ]; then
            rm -rf allure-results/* allure-report/*
            echo -e "${GREEN}✅ 모든 파일이 정리되었습니다${NC}"
        else
            echo -e "${GREEN}✅ 컨테이너만 정리되었습니다${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac

echo ""
echo "===================================="
echo -e "${GREEN}✅ 완료!${NC}"