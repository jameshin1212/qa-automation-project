#!/bin/bash

# Allure Report 생성 및 서버 실행 스크립트

echo "📊 Generating Allure Report..."

# allure-results 디렉토리 확인
if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
    echo "⚠️  allure-results 디렉토리가 비어있거나 존재하지 않습니다."
    echo "먼저 테스트를 실행해주세요:"
    echo "  docker-compose run --rm all-test"
    exit 1
fi

# Allure Report 디렉토리 생성
mkdir -p allure-report

# Allure Report 생성 (Docker 사용)
echo "🔨 Generating report from test results..."
docker run --rm \
  -v $(pwd)/allure-results:/allure-results \
  -v $(pwd)/allure-report:/allure-report \
  frankescobar/allure-docker-service \
  allure generate /allure-results -o /allure-report --clean

# 리포트 생성 확인
if [ ! -f "allure-report/index.html" ]; then
    echo "❌ Allure Report 생성 실패!"
    echo "allure-results 디렉토리를 확인해주세요."
    exit 1
fi

echo "✅ Allure Report 생성 완료!"

# Python 간단한 HTTP 서버로 리포트 제공
echo "🌐 Starting Report Server at http://localhost:8080"
echo "Press Ctrl+C to stop the server"

cd allure-report
python3 -m http.server 8080