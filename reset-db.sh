#!/bin/bash

# Mock Server 데이터베이스 초기화 스크립트

echo "🔄 WhaTap QA - Database Reset"
echo "===================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Mock Server 디렉토리 확인
MOCK_SERVER_DIR="mock_server"
DB_FILE="$MOCK_SERVER_DIR/db.json"
DB_BACKUP="$MOCK_SERVER_DIR/db-backup.json"

# 현재 DB 상태 확인
echo ""
echo "📊 현재 데이터베이스 상태:"
echo "-----------------------------------"

if [ -f "$DB_FILE" ]; then
    # Python을 사용하여 JSON 파싱
    user_count=$(python3 -c "import json; data=json.load(open('$DB_FILE')); print(len(data.get('users', [])))" 2>/dev/null || echo "0")
    echo "• 등록된 사용자 수: ${user_count}명"
    
    if [ "$user_count" -gt 0 ]; then
        echo ""
        echo "📝 등록된 이메일 목록:"
        python3 -c "
import json
try:
    with open('$DB_FILE', 'r') as f:
        data = json.load(f)
        users = data.get('users', [])
        for user in users[:10]:  # 최대 10개만 표시
            print(f\"  - {user.get('email', 'Unknown')}\")
        if len(users) > 10:
            print(f\"  ... 외 {len(users)-10}개\")
except:
    print('  (읽기 실패)')
" 2>/dev/null
    fi
else
    echo -e "${RED}❌ db.json 파일이 없습니다${NC}"
    exit 1
fi

# 초기화 옵션 선택
echo ""
echo "===================================="
echo "초기화 옵션을 선택하세요:"
echo ""
echo "1) 🔄 DB 초기화 (백업에서 복원)"
echo "2) 💾 현재 DB 백업 후 초기화"
echo "3) 🗑️  특정 이메일만 삭제"
echo "4) 🧹 모든 사용자 삭제 (설정은 유지)"
echo "5) 📋 DB 상태만 확인"
echo "6) ❌ 취소"
echo ""
read -p "선택 (1-6): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}🔄 데이터베이스를 초기화합니다...${NC}"
        
        # 백업 파일 확인
        if [ ! -f "$DB_BACKUP" ]; then
            echo -e "${RED}❌ 백업 파일이 없습니다: $DB_BACKUP${NC}"
            exit 1
        fi
        
        # 백업에서 복원
        cp "$DB_BACKUP" "$DB_FILE"
        
        # Mock Server 재시작 여부 확인
        if pgrep -f "node.*server.js" > /dev/null; then
            echo ""
            echo "Mock Server가 실행 중입니다. 재시작하시겠습니까? (y/n)"
            read -p "선택: " restart_choice
            
            if [ "$restart_choice" = "y" ] || [ "$restart_choice" = "Y" ]; then
                echo -e "${YELLOW}Mock Server를 재시작합니다...${NC}"
                pkill -f "node.*server.js"
                sleep 2
                cd "$MOCK_SERVER_DIR" && npm start > ../server.log 2>&1 &
                cd ..
                sleep 3
                echo -e "${GREEN}✅ Mock Server가 재시작되었습니다${NC}"
            fi
        fi
        
        echo -e "${GREEN}✅ 데이터베이스가 초기화되었습니다${NC}"
        ;;
        
    2)
        echo ""
        echo -e "${YELLOW}💾 현재 DB를 백업하고 초기화합니다...${NC}"
        
        # 타임스탬프로 백업
        timestamp=$(date +"%Y%m%d_%H%M%S")
        backup_file="$MOCK_SERVER_DIR/db-backup-$timestamp.json"
        cp "$DB_FILE" "$backup_file"
        echo "  • 백업 완료: $backup_file"
        
        # 초기화
        cp "$DB_BACKUP" "$DB_FILE"
        echo -e "${GREEN}✅ 데이터베이스가 초기화되었습니다${NC}"
        ;;
        
    3)
        echo ""
        echo "삭제할 이메일 주소를 입력하세요:"
        read -p "이메일: " email_to_delete
        
        if [ -z "$email_to_delete" ]; then
            echo -e "${RED}❌ 이메일을 입력하세요${NC}"
            exit 1
        fi
        
        # Python으로 특정 이메일 삭제
        python3 -c "
import json

with open('$DB_FILE', 'r') as f:
    data = json.load(f)

original_count = len(data.get('users', []))
data['users'] = [u for u in data.get('users', []) if u.get('email') != '$email_to_delete']
removed_count = original_count - len(data['users'])

with open('$DB_FILE', 'w') as f:
    json.dump(data, f, indent=2)

if removed_count > 0:
    print(f'✅ {removed_count}개 계정이 삭제되었습니다')
else:
    print('❌ 해당 이메일을 찾을 수 없습니다')
" 2>/dev/null
        ;;
        
    4)
        echo ""
        echo -e "${YELLOW}🧹 모든 사용자를 삭제합니다...${NC}"
        echo "정말로 모든 사용자를 삭제하시겠습니까? (yes/no)"
        read -p "확인: " confirm
        
        if [ "$confirm" = "yes" ]; then
            # Python으로 users 배열만 비우기
            python3 -c "
import json

with open('$DB_FILE', 'r') as f:
    data = json.load(f)

user_count = len(data.get('users', []))
data['users'] = []

with open('$DB_FILE', 'w') as f:
    json.dump(data, f, indent=2)

print(f'✅ {user_count}개 계정이 삭제되었습니다')
" 2>/dev/null
        else
            echo -e "${BLUE}ℹ️  취소되었습니다${NC}"
        fi
        ;;
        
    5)
        echo ""
        echo -e "${BLUE}ℹ️  상태 확인만 완료되었습니다${NC}"
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

# 초기화 후 상태 확인
if [ "$choice" != "5" ] && [ "$choice" != "6" ]; then
    echo ""
    echo "===================================="
    echo "초기화 후 데이터베이스 상태:"
    echo "-----------------------------------"
    
    user_count=$(python3 -c "import json; data=json.load(open('$DB_FILE')); print(len(data.get('users', [])))" 2>/dev/null || echo "0")
    echo "• 등록된 사용자 수: ${user_count}명"
fi

echo ""
echo "===================================="
echo -e "${GREEN}✅ 완료!${NC}"
echo ""
echo "💡 테스트를 다시 실행하려면:"
echo "   pytest tests/api/test_registration_duplicate.py -v"
echo "   또는"
echo "   ./run_tests.sh"