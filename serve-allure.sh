#!/bin/bash

# Allure Report 로컬 서버 실행 스크립트

echo "📊 WhaTap QA - Allure Report Server"
echo "===================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Python 확인
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python이 설치되지 않았습니다.${NC}"
    exit 1
fi

# Allure Report 디렉토리 확인
if [ ! -d "allure-report" ]; then
    echo -e "${RED}❌ allure-report 디렉토리가 없습니다.${NC}"
    echo "먼저 Allure Report를 생성하세요:"
    echo "  ./docker-allure.sh (옵션 1 또는 2)"
    exit 1
fi

# 실행 옵션 선택
echo ""
echo "Allure Report 서버 실행 방법을 선택하세요:"
echo "1) 🐍 Python HTTP Server (간단)"
echo "2) 🔥 Allure Serve (권장)"
echo "3) 🐳 Docker Allure Server"
echo "4) 📂 파일 탐색기로 열기 (제한적)"
read -p "선택 (1-4): " choice

case $choice in
    1)
        echo -e "${GREEN}✅ Python HTTP Server를 시작합니다${NC}"
        echo -e "${BLUE}브라우저에서 열기: http://localhost:8080${NC}"
        echo -e "${YELLOW}종료: Ctrl+C${NC}"
        echo ""
        
        cd allure-report
        $PYTHON_CMD -m http.server 8080
        ;;
        
    2)
        echo -e "${GREEN}✅ Allure Serve를 시작합니다${NC}"
        
        # Allure 설치 확인
        if ! command -v allure &> /dev/null; then
            echo -e "${RED}❌ Allure가 설치되지 않았습니다.${NC}"
            echo "설치 방법:"
            echo "  Mac: brew install allure"
            echo "  또는 Docker 사용: ./docker-allure.sh (옵션 3)"
            exit 1
        fi
        
        echo -e "${BLUE}브라우저에서 자동으로 열립니다...${NC}"
        echo -e "${YELLOW}종료: Ctrl+C${NC}"
        echo ""
        
        # allure-results에서 직접 serve
        allure serve allure-results
        ;;
        
    3)
        echo -e "${GREEN}✅ Docker Allure Server를 시작합니다${NC}"
        echo -e "${BLUE}브라우저에서 열기: http://localhost:5050${NC}"
        echo -e "${YELLOW}종료: Ctrl+C${NC}"
        echo ""
        
        docker-compose run --rm -p 5050:5050 test-runner bash -c "
            allure serve /app/allure-results -p 5050 --host 0.0.0.0
        "
        ;;
        
    4)
        echo -e "${YELLOW}⚠️ 파일로 직접 열기 (제한된 기능)${NC}"
        echo -e "${RED}CORS 문제로 일부 데이터가 로드되지 않을 수 있습니다.${NC}"
        echo ""
        
        # Chrome에서 보안 비활성화로 열기 (macOS)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Chrome을 보안 비활성화 모드로 실행하시겠습니까? (y/n)"
            echo -e "${RED}⚠️ 주의: 이 모드는 보안이 비활성화됩니다. 테스트 후 Chrome을 완전히 종료하세요.${NC}"
            read -p "선택: " chrome_choice
            
            if [ "$chrome_choice" = "y" ] || [ "$chrome_choice" = "Y" ]; then
                # Chrome 종료
                osascript -e 'quit app "Google Chrome"'
                sleep 2
                
                # 보안 비활성화 모드로 실행
                open -a "Google Chrome" --args --disable-web-security --user-data-dir=/tmp/chrome_dev_test --allow-file-access-from-files "file://$(pwd)/allure-report/index.html"
                
                echo -e "${GREEN}✅ Chrome이 보안 비활성화 모드로 실행되었습니다${NC}"
                echo -e "${RED}⚠️ 테스트 후 반드시 Chrome을 완전히 종료하세요!${NC}"
            else
                open allure-report/index.html
            fi
        else
            echo "파일 경로: $(pwd)/allure-report/index.html"
            echo "브라우저에서 위 경로를 직접 열어주세요."
        fi
        ;;
        
    *)
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac