#!/bin/bash

# Allure Report 생성 및 서버 실행 스크립트

echo "📊 Generating Allure Report..."

# Allure Report 생성 (Docker 사용)
docker run --rm \
  -v $(pwd)/allure-results:/app/allure-results \
  -v $(pwd)/allure-report:/app/allure-report \
  frankescobar/allure-docker-service \
  allure generate /app/allure-results -o /app/allure-report --clean

# Python 간단한 HTTP 서버로 리포트 제공
echo "🌐 Starting Report Server at http://localhost:8080"
echo "Press Ctrl+C to stop the server"

cd allure-report
python3 -m http.server 8080