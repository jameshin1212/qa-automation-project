#!/bin/bash

# API Test Inspector 실행 스크립트
# 각 API 테스트케이스의 Request와 Response를 확인

echo "🔍 API Test Inspector"
echo "===================="

# Check if server is running
if ! docker ps | grep -q qa-server; then
    echo "⚠️  QA Server is not running. Starting server..."
    docker-compose up -d qa-server
    echo "Waiting for server to start..."
    sleep 5
fi

# Install required packages if needed
pip install -q requests colorama 2>/dev/null || true

# Run the inspector
echo ""
echo "Running API test inspection..."
echo ""

# Use Docker environment URL
python3 test_api_inspector.py http://localhost:3000

echo ""
echo "✅ Inspection complete!"