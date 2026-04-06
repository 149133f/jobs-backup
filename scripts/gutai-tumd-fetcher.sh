#!/bin/bash
# 股泰驛站 TUMD 資料抓取腳本
# 抓取 UA Analyze 的 TUMD 數據
# 週六7點後不報 → 週一5點後開始報

# 取得現在時間
WEEKDAY=$(date +%u)  # 1=週一 ~ 7=週日
HOUR=$(date +%H)
MIN=$(date +%M)

# 轉換成分鐘
CURRENT_MIN=$((10#$HOUR * 60 + 10#$MIN))
FIVE_AM=300   # 05:00 = 300分
SEVEN_AM=420  # 07:00 = 420分

# 週六(6) 07:00 後不報
if [ "$WEEKDAY" -eq 6 ] && [ "$CURRENT_MIN" -ge $SEVEN_AM ]; then
    echo "週六7點後不報價 (現在: 週六 $HOUR:$MIN)"
    exit 0
fi

# 週日(7) 全天不報
if [ "$WEEKDAY" -eq 7 ]; then
    echo "週日不報價 (現在: 週日 $HOUR:$MIN)"
    exit 0
fi

# 週一(1) 05:00 前不報
if [ "$WEEKDAY" -eq 1 ] && [ "$CURRENT_MIN" -lt $FIVE_AM ]; then
    echo "週一5點前不報價 (現在: 週一 $HOUR:$MIN)"
    exit 0
fi

# 嘗試抓取 UA Analyze 頁面
# 使用 curl 抓取頁面
UA_URL="https://pro.uanalyze.com.tw/lab/dashboard/32775"
RESULT=$(curl -s -L --max-time 10 "$UA_URL" 2>&1)

# 檢查是否成功取得內容
if echo "$RESULT" | grep -q "TU\|TM\|TD\|WD\|MD"; then
    # 提取 TUMD 數據
    TUMD_DATA=$(echo "$RESULT" | grep -oE "TU[0-9,]+|TM[0-9,]+|TD[0-9,]+|WD[0-9,]+|MD[0-9,]+" | tr '\n' ' ')
    echo "📊 股泰驛站 TUMD 資料：$TUMD_DATA"
else
    # 無法取得結構化數據，嘗試用瀏覽器截圖
    echo "⚠️ 無法直接取得 TUMD 數據，切換到瀏覽器截圖模式"
    
    # 嘗試使用 Chrome CDP 截圖
    SCREENSHOT_FILE="/tmp/tumd_screenshot_$(date +%Y%m%d_%H%M%S).png"
    
    # 嘗試用 Python playwright 或直接用 curl 調用 CDP
    python3 << 'PYEOF'
import subprocess
import json
import time

try:
    # 嘗試直接用 CDP 截圖
    import urllib.request
    
    # 取得 CDP session
    cdp_url = "http://127.0.0.1:9224/json"
    
    # 嘗試連接
    with urllib.request.urlopen(cdp_url, timeout=5) as response:
        tabs = json.loads(response.read())
        if tabs:
            target = tabs[0]
            ws_url = target.get('webSocketDebuggerUrl')
            print(f"找到 Chrome: {target.get('title', 'Unknown')}")
            
            # 這裡需要用 CDP protocol 發送命令
            # 比較複雜，先用備用方案
            
except Exception as e:
    print(f"CDP 連接失敗: {e}")
    print("需要手動截圖")
PYEOF
    
    echo "📸 請手動截圖：$UA_URL"
fi

# 輸出時間戳
echo "抓取時間：$(date '+%Y-%m-%d %H:%M:%S')"
