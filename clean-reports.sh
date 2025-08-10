#!/bin/bash

# 테스트 결과 및 리포트 초기화 스크립트

echo "🧹 WhaTap QA - Test Reports Cleaner"
echo "===================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 상태 확인
echo ""
echo "📊 현재 상태:"
echo "-----------------------------------"

# Allure Results 확인
if [ -d "allure-results" ]; then
    count=$(ls -1 allure-results/*.json 2>/dev/null | wc -l)
    echo "• Allure Results: ${count} 파일"
else
    echo "• Allure Results: 디렉토리 없음"
fi

# Allure Report 확인
if [ -d "allure-report" ]; then
    if [ -f "allure-report/index.html" ]; then
        echo "• Allure Report: 생성됨"
    else
        echo "• Allure Report: 비어있음"
    fi
else
    echo "• Allure Report: 디렉토리 없음"
fi

# Reports 디렉토리 확인
if [ -d "reports" ]; then
    count=$(ls -1 reports/* 2>/dev/null | wc -l)
    echo "• Reports: ${count} 파일"
else
    echo "• Reports: 디렉토리 없음"
fi

# pytest cache 확인
if [ -d ".pytest_cache" ]; then
    echo "• Pytest Cache: 있음"
else
    echo "• Pytest Cache: 없음"
fi

# 정리 옵션 선택
echo ""
echo "===================================="
echo "정리할 항목을 선택하세요:"
echo ""
echo "1) 🗑️  Allure Results만 삭제"
echo "2) 📄 Allure Report만 삭제"
echo "3) 🧹 Allure 관련 모두 삭제 (Results + Report)"
echo "4) 🗂️  Reports 디렉토리 정리"
echo "5) 🔥 전체 초기화 (모든 테스트 결과)"
echo "6) ❌ 취소"
echo ""
read -p "선택 (1-6): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}🗑️  Allure Results를 삭제합니다...${NC}"
        if [ -d "allure-results" ]; then
            rm -rf allure-results/*
            echo -e "${GREEN}✅ Allure Results가 삭제되었습니다${NC}"
        else
            echo -e "${BLUE}ℹ️  삭제할 파일이 없습니다${NC}"
        fi
        ;;
        
    2)
        echo ""
        echo -e "${YELLOW}📄 Allure Report를 삭제합니다...${NC}"
        if [ -d "allure-report" ]; then
            rm -rf allure-report/*
            echo -e "${GREEN}✅ Allure Report가 삭제되었습니다${NC}"
        else
            echo -e "${BLUE}ℹ️  삭제할 파일이 없습니다${NC}"
        fi
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}🧹 Allure 관련 파일을 모두 삭제합니다...${NC}"
        
        # Allure Results 삭제
        if [ -d "allure-results" ]; then
            rm -rf allure-results/*
            echo "  • Allure Results 삭제됨"
        fi
        
        # Allure Report 삭제
        if [ -d "allure-report" ]; then
            rm -rf allure-report/*
            echo "  • Allure Report 삭제됨"
        fi
        
        echo -e "${GREEN}✅ Allure 파일이 모두 삭제되었습니다${NC}"
        ;;
        
    4)
        echo ""
        echo -e "${YELLOW}🗂️  Reports 디렉토리를 정리합니다...${NC}"
        if [ -d "reports" ]; then
            rm -rf reports/*
            echo -e "${GREEN}✅ Reports 디렉토리가 정리되었습니다${NC}"
        else
            echo -e "${BLUE}ℹ️  삭제할 파일이 없습니다${NC}"
        fi
        ;;
        
    5)
        echo ""
        echo -e "${RED}⚠️  경고: 모든 테스트 결과가 삭제됩니다!${NC}"
        echo "정말로 전체 초기화를 진행하시겠습니까? (yes/no)"
        read -p "확인: " confirm
        
        if [ "$confirm" = "yes" ]; then
            echo ""
            echo -e "${YELLOW}🔥 전체 초기화를 진행합니다...${NC}"
            
            # Allure Results 삭제
            if [ -d "allure-results" ]; then
                rm -rf allure-results/*
                echo "  • Allure Results 삭제됨"
            fi
            
            # Allure Report 삭제
            if [ -d "allure-report" ]; then
                rm -rf allure-report/*
                echo "  • Allure Report 삭제됨"
            fi
            
            # Reports 디렉토리 삭제
            if [ -d "reports" ]; then
                rm -rf reports/*
                echo "  • Reports 디렉토리 정리됨"
            fi
            
            # Pytest Cache 삭제
            if [ -d ".pytest_cache" ]; then
                rm -rf .pytest_cache
                echo "  • Pytest Cache 삭제됨"
            fi
            
            # __pycache__ 삭제
            find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
            echo "  • Python Cache 삭제됨"
            
            echo ""
            echo -e "${GREEN}✅ 모든 테스트 결과가 초기화되었습니다${NC}"
        else
            echo -e "${BLUE}ℹ️  초기화가 취소되었습니다${NC}"
        fi
        ;;
        
    6)
        echo ""
        echo -e "${BLUE}ℹ️  취소되었습니다${NC}"
        exit 0
        ;;
        
    *)
        echo ""
        echo -e "${RED}❌ 잘못된 선택입니다${NC}"
        exit 1
        ;;
esac

# 정리 후 상태 확인
echo ""
echo "===================================="
echo "정리 후 상태:"
echo "-----------------------------------"

# Allure Results 확인
if [ -d "allure-results" ]; then
    count=$(ls -1 allure-results/*.json 2>/dev/null | wc -l)
    echo "• Allure Results: ${count} 파일"
else
    echo "• Allure Results: 디렉토리 없음"
fi

# Allure Report 확인
if [ -d "allure-report" ]; then
    if [ -f "allure-report/index.html" ]; then
        echo "• Allure Report: 생성됨"
    else
        echo "• Allure Report: 비어있음"
    fi
else
    echo "• Allure Report: 디렉토리 없음"
fi

echo ""
echo "===================================="
echo -e "${GREEN}✅ 완료!${NC}"
echo ""
echo "💡 새로운 테스트를 실행하려면:"
echo "   pytest tests/api -v --alluredir=allure-results"
echo "   또는"
echo "   ./run_with_allure.sh"