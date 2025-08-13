#!/bin/bash

# 간단한 Allure Report 생성 및 실행 스크립트

echo "📊 Allure Report 생성 중..."

# allure-results가 있는지 확인
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
    echo "⚠️  테스트 결과가 없습니다. 먼저 테스트를 실행하세요:"
    echo "  docker-compose run --rm all-test"
    exit 1
fi

# 기존 리포트 삭제
rm -rf allure-report

# Docker를 사용하여 리포트 생성
docker run --rm \
    -v $(pwd):/workspace \
    -w /workspace \
    openjdk:11-jre-slim \
    sh -c "
        apt-get update && apt-get install -y wget unzip &&
        wget -q https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip &&
        unzip -q allure-2.27.0.zip &&
        ./allure-2.27.0/bin/allure generate allure-results -o allure-report --clean
    "

# 생성 확인
if [ -f "allure-report/index.html" ]; then
    echo "✅ Allure Report 생성 완료!"
    echo ""
    echo "🌐 리포트 서버 시작중..."
    echo "📍 브라우저에서 http://localhost:8080 접속"
    echo "종료하려면 Ctrl+C를 누르세요"
    echo ""
    cd allure-report && python3 -m http.server 8080
else
    echo "❌ 리포트 생성 실패"
fi