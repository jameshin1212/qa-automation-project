#!/bin/bash

# UI 테스트를 로컬 환경에서 브라우저 모드로 실행하는 스크립트

echo "🚀 Starting UI Tests in Browser Mode"
echo "===================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Mock 서버가 실행 중인지 확인
check_mock_server() {
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Mock 서버 시작
start_mock_server() {
    echo -e "${YELLOW}📦 Starting Mock Server...${NC}"
    cd mock_server
    
    # db.json 백업 복원
    cp db-backup.json db.json
    echo -e "${GREEN}✅ Database initialized from backup${NC}"
    
    # Mock 서버 백그라운드 실행
    npm start > ../server.log 2>&1 &
    SERVER_PID=$!
    echo "Mock server PID: $SERVER_PID"
    
    # 서버 시작 대기
    echo -n "Waiting for mock server to start..."
    for i in {1..10}; do
        if check_mock_server; then
            echo -e " ${GREEN}Ready!${NC}"
            cd ..
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    echo -e " ${RED}Failed to start!${NC}"
    cd ..
    return 1
}

# Playwright 브라우저 설치 확인
check_playwright() {
    if [ ! -d "$HOME/Library/Caches/ms-playwright" ]; then
        echo -e "${YELLOW}📥 Installing Playwright browsers...${NC}"
        playwright install chromium
    fi
}

# 메인 실행
main() {
    # Python 가상환경 확인
    if [ -z "$VIRTUAL_ENV" ]; then
        echo -e "${YELLOW}⚠️  Python virtual environment not activated${NC}"
        echo "Please run: source venv/bin/activate"
        exit 1
    fi
    
    # Mock 서버 확인 및 시작
    if ! check_mock_server; then
        if ! start_mock_server; then
            echo -e "${RED}❌ Failed to start mock server${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Mock server already running${NC}"
    fi
    
    # Playwright 브라우저 확인
    check_playwright
    
    # UI 테스트 실행
    echo -e "${GREEN}🧪 Running UI Tests with Browser...${NC}"
    echo "Options:"
    echo "  --headed: Show browser window"
    echo "  --slowmo=1000: Slow down actions by 1 second"
    echo ""
    
    # 테스트 실행
    pytest tests/ui/ --headed --slowmo=1000 -v
    TEST_EXIT_CODE=$?
    
    # 결과 출력
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All UI tests passed!${NC}"
    else
        echo -e "${RED}❌ Some tests failed${NC}"
    fi
    
    # Mock 서버 종료 옵션
    echo ""
    read -p "Stop mock server? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ ! -z "$SERVER_PID" ]; then
            kill $SERVER_PID 2>/dev/null
            echo -e "${GREEN}✅ Mock server stopped${NC}"
        else
            # PID가 없으면 포트로 찾아서 종료
            lsof -ti:3000 | xargs kill 2>/dev/null
            echo -e "${GREEN}✅ Mock server stopped${NC}"
        fi
    fi
    
    exit $TEST_EXIT_CODE
}

# 스크립트 실행
main