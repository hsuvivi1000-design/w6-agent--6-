# w6-agent--6-

# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題：生活顧問

---

## Agent 功能總覽

> 這個 Agent 是一個「生活顧問」，使用者輸入城市名稱後，
> Agent 會自動呼叫天氣工具查詢即時天氣，並根據天氣狀況判斷適合室內或室外活動，
> 最後推薦 3-5 個具體的活動建議以及隨機冷笑話和趣味冷知識。

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| （例：天氣） | 呼叫 weather_tool，查詢即時天氣        |  朱覺祥  |
| （例：笑話） | 呼叫 joke_tool，取得隨機英文笑話(附中文翻譯)  |  林湘紜  |
| （例：建議） | 呼叫 advice_tool，取得隨機建議         | 林伽紜    |
| （例：冷知識） | 執行 fun_fact_tool，取得趣味冷知識     |  許瀞云   |

---

## 組員與分工

| 姓名   | 負責功能             | 檔案                     | 使用的 API             |
| ------ | -------------------- | ------------------------ | ---------------------- |
| 林伽紜 | 取得一則今日人生建議        | `tools/advice_tool.py`  | https://api.adviceslip.com/advice                |
| 朱覺祥 | 天氣查詢 Tool        | `tools/weather_tool.py`  | wttr.in                 |
| 林湘紜 |  取得每日一笑話      | `tools/joke_tool.py`  |  icanhazdadjoke    |
| 許瀞云 |  取得一則趣味冷知識      | `tools/fun_fact_tool.py`  |  Useless Facts    |
| 許瀞云| Skill 整合           | `skills/`                | —                      |
| 朱覺祥| Agent 主程式         | `main.py`                | Gemini API             |

---

## 專案架構

```
├── tools/
│   ├── advice_tool.py   
│   ├── xxx_tool.py   
│   └── joke_tool.py  
│   ├── __init__.py          # tools 套件初始化
│   └── weather_tool.py      # 天氣查詢工具（wttr.in）
├── skills/
│   └── (待新增)
├── main.py                  # Agent 主程式（Gemini Function Calling）
├── requirements.txt         # Python 依賴套件
├── .env                     # API Key 設定（不上傳）
├── .env.example             # API Key 範例
└── README.md
```

---

## 使用方式

```bash
# 1. 建立虛擬環境
python -m venv .venv

# 2. 啟動虛擬環境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 3. 安裝依賴套件
pip install -r requirements.txt

# 4. 設定 API Key（複製範例檔並填入你的金鑰）
copy .env.example .env
# 編輯 .env，填入你的 GEMINI_API_KEY

# 5. 執行 Agent
python main.py
```

---

## 執行結果

> Agent 執行時會清楚顯示每個步驟的工具調用過程：

```

╔══════════════════════════════════════════════════════╗
║          🌿  健康生活顧問 AI Agent  🌿              ║
║                                                      ║
║   試試看輸入「幫我規劃今天」或任何健康生活問題！    ║
║   輸入 'quit' 或 'exit' 離開                         ║
╚══════════════════════════════════════════════════════╝

🗣️  請輸入 ▸ 幫我規劃今天

  👤  使用者輸入
      │ 幫我規劃今天


  🤖  正在思考中...
      │ 將訊息送給 Gemini API


  💬  Agent 最終回覆
      ╭──────────────────────────────────────────────────╮       
      │ 好的！沒問題 ☀️ 為了幫你規劃最適合你的一天，請先告訴我你  所在的城市是哪裡呢？ 😊
      ╰──────────────────────────────────────────────────╯       

🗣️  請輸入 ▸ 台中西屯

  👤  使用者輸入
      │ 台中西屯


  🤖  正在思考中...
      │ 將訊息送給 Gemini API


  💬  Agent 最終回覆
      ╭──────────────────────────────────────────────────╮       
      │ 收到！這就來幫你查詢台中的天氣，並為你準備一份專屬的健康 生活計畫！ 📝 請稍等我一下喔～ 💨
      ╰──────────────────────────────────────────────────╯       


  🤖  正在思考中...
      │ 將訊息送給 Gemini API


  💬  Agent 最終回覆
      ╭──────────────────────────────────────────────────╮       
      │ 太好了！台中西屯的天氣資訊已經準備好了，我也為你準備了一 份充滿能量的「今日健康生活計畫」！ 🌟 讓我們一起來看看吧！       
      │
      │ ---
      │ 🌿 **今日健康生活計畫**
      │
      │ ☀️ **天氣概況**：
      │ 今天台中西屯的天氣相當不錯！溫度宜人，降雨機率低，也沒有 強風，非常適合進行戶外活動喔！ 😎
      │
      │ 🏃 **活動建議**：
      │ 由於天氣晴朗，我推薦你多到戶外走走，享受陽光和新鮮空氣： 
      │ *   **晨間散步或慢跑**：在公園或河濱步道，用輕快的步伐開 始新的一天。 🚶‍♀️
      │ *   **戶外瑜珈或伸展**：找個舒適的草地，跟著陽光一起舒展 身心。 🧘‍♂️
      │ *   **單車騎行**：探索你家附近的街道或自行車道，感受微風 拂面。 🚲
      │ *   **午間外出用餐或小憩**：到家附近的咖啡廳或公園，享受 悠閒的午後時光。 ☕
      │ *   **傍晚的戶外運動**：可以選擇打球、飛盤，或和朋友來一 場輕鬆的健走。 🏸
      │
      │ 💪 **今日正能量**：
      │ 「The best way to predict the future is to create it.」  
      │ 這句話的意思是，與其擔心未來會怎樣，不如現在就積極地去創 造你想要的未來！今天就讓我們帶著這份積極的心，為自己的目標採取一 些行動吧！ ✨
      │
      │ 😂 **每日一笑**：
      │ Why don't scientists trust atoms?
      │ Because they make up everything!
      │ （為什麼科學家不相信原子？因為它們構成了一切！）
      │ 希望這個笑話能讓你嘴角上揚！ 😄
      │
      │ 💡 **今日冷知識**：
      │ 你知道嗎？章魚有三個心臟！兩個心臟負責將血液泵送到鰓部， 另一個則負責將血液輸送到身體的其他部位。是不是很神奇？ 🐙        
      │
      │ 📋 **建議作息**：
      │ *   **07:00** 起床，喝一杯溫開水，做些簡單的伸展。       
      │ *   **07:30** 享受一頓營養豐富的早餐。 🍳
      │ *   **08:00 - 11:00** 進行晨間戶外活動，如散步或慢跑。   
      │ *   **11:00 - 12:00** 稍微休息，準備午餐。
      │ *   **12:00 - 13:00** 享用午餐，並可安排短暫的戶外散步。 
      │ *   **13:00 - 17:00** 專注於工作或學習，中間可安排短暫休 息，起身走動。
      │ *   **17:00 - 18:30** 進行傍晚的戶外運動或與朋友相聚。   
      │ *   **18:30 - 19:30** 準備並享用晚餐。 🥗
      │ *   **19:30 - 21:30** 閱讀、聽音樂、或進行一些輕鬆的室內 活動。 🎶
      │ *   **21:30** 開始準備睡前儀式，放鬆身心。
      │ *   **22:00** 準備入睡，確保充足的睡眠。 😴
      │
      │ 希望這份計畫能幫助你度過一個健康又愉快的一天！如果你有任 何想調整的地方，隨時告訴我喔！ 😉
      ╰──────────────────────────────────────────────────╯       

```

---

## 各功能說明

### [今日人生建議]（負責：林伽紜）

- **Tool 名稱**：feature/advice-tool
- **使用 API**：https://api.adviceslip.com/advice
- **輸入**：建議
- **輸出範例**：🤖 顧問：今日人生建議：沈默的人往往最深不可測。


### 天氣查詢 Tool（負責：朱覺祥）

- **Tool 名稱**：`get_weather`
- **使用 API**：[wttr.in](https://wttr.in/) — 免費天氣查詢 API
- **輸入**：城市名稱（string），例如 `Taipei`、`Tokyo`、`New York`
- **輸出範例**：

```json
{
  "city": "Taipei",
  "temperature_c": "19",
  "feels_like_c": "19",
  "humidity": "94",
  "weather_desc": "Light rain, 薄霧",
  "wind_speed_kmh": "6",
  "wind_dir": "NNE",
  "uv_index": "1",
  "visibility_km": "6",
  "pressure_mb": "1016",
  "cloud_cover": "100",
  "precip_mm": "0.1",
  "chance_of_rain_pct": 80,
  "max_temp_c": "22",
  "min_temp_c": "17"
}
```

- **Gemini Function Declaration**：

```python
WEATHER_TOOL_DECLARATION = {
    "name": "get_weather",
    "description": "取得指定城市的即時天氣資訊，包含溫度、體感溫度、濕度、天氣描述、風速、降雨機率等。用來判斷適合室內或室外活動。",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "要查詢天氣的城市名稱，例如 Taipei、Tokyo、New York"
            }
        },
        "required": ["city"]
    }
}
```

- **Agent 判斷邏輯**（定義在 system prompt 中）：

| 條件                   | 判定     |
| ---------------------- | -------- |
| 降雨機率 > 60%         | 室內活動 |
| 溫度 > 35°C 或 < 5°C  | 室內活動 |
| 風速 > 40 km/h         | 室內活動 |
| 其他情況               | 室外活動 |

### [每日笑話]（負責：林湘紜）

- **Tool 名稱**：joke_tool
- **使用 API**：icanhazdadjoke
- **輸入**：給我一個笑話
- **輸出範例**：🤖 顧問：為什麼雞蛋不會講笑話？ 他們會互相攻擊(They'd crack each other up)

### [趣味冷知識]（負責：許瀞云）

- **Tool 名稱**：fun_fact_tool
- **使用 API**：Useless Facts
- **輸入**：給我一個冷知識
- **輸出範例**：🤖 顧問：你知道嗎？章魚有三個心臟！兩個心臟負責將血液泵送到鰓部，另一個則負責將血液輸送到身體的其他部位。是不是很神奇？ 🐙

### Skill：[daily_health_plan]（負責：許瀞云）

- **組合了哪些 Tool**：feature/advice-tool、get_weather、joke_tool、fun_fact_tool
- **執行順序**：

```
Step 1: 呼叫 get_weather → 取得天氣
Step 2: 呼叫 feature/advice-tool → 取得人生建議
Step 3: 呼叫 joke_tool → 取得笑話
Step 4: 呼叫 fun_fact_tool → 取得冷知識
Step 5: 組合輸出 → 產生今日人生建議
```

---

## 心得

### 遇到最難的問題


最大的困難是 Gemini chat.send_message() 回傳 function response 時格式要求與文件不同，需改用 types.Part 直接傳遞而非包在 types.Content 裡，花了一些時間除錯才解決。

忘記改gemini調用的版本，一直和我說我額度沒了，差點害我嚇死

### Tool 和 Skill 的差別

Tool是一個單一功能的函式，skill是多個 Tool 組合起來的工作流程

### 如果再加一個功能

可能再加入地圖和規劃路線吧，剛好配合天氣！
