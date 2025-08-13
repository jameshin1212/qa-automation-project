#!/bin/bash

# Docker 테스트 실행 스크립트
echo "🚀 Starting WhaTap QA Automation Tests with Docker"
echo "================================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 기존 컨테이너 정리
echo -e "${YELLOW}🧹 Cleaning up existing containers...${NC}"
docker-compose down

# Docker 이미지 빌드
echo -e "${YELLOW}🔨 Building Docker images...${NC}"
docker-compose build

# Mock 서버 시작
echo -e "${GREEN}📦 Starting Mock Server...${NC}"
docker-compose up -d qa-server

# 서버가 준비될 때까지 대기
echo "⏳ Waiting for Mock Server to be ready..."
sleep 10

# API 테스트 실행
echo -e "${GREEN}🧪 Running API Tests...${NC}"
docker-compose run --rm api-test

# UI 테스트 실행  
echo -e "${GREEN}🖥️ Running UI Tests...${NC}"
docker-compose run --rm ui-test

# Allure Report 서버 시작
echo -e "${GREEN}📊 Starting Allure Report Server...${NC}"
docker-compose up -d allure-report

echo "================================================"
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "📊 View test results:"
echo "   - Allure Report: http://localhost:5050"
echo "   - API Documentation: http://localhost:4040"
echo ""
echo "🧹 To cleanup, run: docker-compose down"