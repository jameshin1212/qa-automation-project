#!/bin/bash

# Docker test runner script
# This script ensures proper test execution in Docker environment

echo "🚀 Starting WhaTap QA Automation Tests in Docker..."

# Start mock server in background
echo "📦 Starting Mock Server..."
cd /app/mock_server
npm start &
SERVER_PID=$!

# Wait for server to be ready
echo "⏳ Waiting for Mock Server to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:3000/config > /dev/null 2>&1; then
        echo "✅ Mock Server is ready!"
        # Test the /api/register endpoint
        curl -s -X POST http://localhost:3000/api/register \
            -H "Content-Type: application/json" \
            -d '{"email":"test@test.com","password":"Test1234!"}' > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ /api/register endpoint is working!"
        else
            echo "⚠️  /api/register endpoint might have issues"
        fi
        break
    fi
    echo "Waiting for server... ($i/30)"
    sleep 1
done

# Run tests
echo "🧪 Running tests..."
cd /app
pytest -v

# Get test exit code
TEST_EXIT_CODE=$?

# Kill mock server
kill $SERVER_PID 2>/dev/null

# Generate Allure report if tests were run
if [ -d allure-results ] && [ "$(ls -A allure-results)" ]; then
    echo "📊 Generating Allure report..."
    allure generate allure-results -o allure-report --clean
    echo "📊 Allure report generated at /app/allure-report"
fi

# Exit with test exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests passed successfully!"
else
    echo "❌ Some tests failed. Check the output above."
fi

exit $TEST_EXIT_CODE