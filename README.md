# w6-agent--6-

# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題： 旅遊前哨站 /  偵探事務所 /  生活顧問

---

## Agent 功能總覽

> 這個 Agent 是一個「天氣生活顧問」，使用者輸入城市名稱或天氣相關問題後，
> Agent 會自動呼叫天氣工具查詢即時天氣，並根據天氣狀況判斷適合室內或室外活動，
> 最後推薦 3-5 個具體的活動建議。

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| （例：天氣） | 呼叫 weather_tool，查詢即時天氣        |  朱覺祥  |
| （例：景點） | 呼叫 search_tool，搜尋熱門景點         |          |
| （例：建議） | 呼叫 advice_tool，取得隨機建議         |          |
| （例：出發） | 執行 trip_briefing Skill，產出行前簡報 |          |

---

## 組員與分工

| 姓名   | 負責功能             | 檔案                     | 使用的 API             |
| ------ | -------------------- | ------------------------ | ---------------------- |
| 朱覺祥 | 天氣查詢 Tool        | `tools/weather_tool.py`  | wttr.in                |
|        |                      | `tools/`                 |                        |
|        |                      | `tools/`                 |                        |
|        | Skill 整合           | `skills/`                | —                      |
|        | Agent 主程式         | `main.py`                | Gemini API             |

---

## 專案架構

```
├── tools/
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
║          🌤️  天氣生活顧問 AI Agent  🌤️              ║
║                                                      ║
║   查詢任何城市的天氣，AI 幫你決定今天適合做什麼！    ║
║   輸入 'quit' 或 'exit' 離開                         ║
╚══════════════════════════════════════════════════════╝

🗣️  請輸入 ▸ 台中市今天天氣怎樣？適合什麼活動？

  👤  使用者輸入
      │ 台中市今天天氣怎樣？適合什麼活動？

  🤖  正在思考中...
      │ 將訊息送給 Gemini API

  🔧  Agent 決定呼叫工具: get_weather
      │ 參數: {
      │   "city": "Taichung"
      │ }

  📊  工具回傳結果 (get_weather)
      │ {
      │   "city": "Taichung",
      │   "temperature_c": "21",
      │   "feels_like_c": "21",
      │   "humidity": "94",
      │   "weather_desc": "Light rain, 薄霧",
      │   "wind_speed_kmh": "6",
      │   "uv_index": "4",
      │   "chance_of_rain_pct": 80,
      │   "max_temp_c": "26",
      │   "min_temp_c": "21"
      │ }

  🔄  將工具結果回傳給 Gemini...

  💬  Agent 最終回覆
      ╭──────────────────────────────────────────────────╮
      │ 🌧️ 台中市今天天氣概況：
      │ 目前溫度 21°C，體感溫度 21°C，濕度 94%，
      │ 天氣狀況為小雨伴隨薄霧，降雨機率高達 80%。
      │
      │ 🏠 判定結果：建議【室內活動】
      │ （降雨機率 80% > 60%，加上濕度高、有霧）
      │
      │ 📋 推薦活動：
      │ 1. 🎬 到電影院看場好電影
      │ 2. ☕ 找間咖啡廳悠閒閱讀
      │ 3. 🎨 參觀台中國立美術館
      │ 4. 🛍️ 到大型商場逛街購物
      │ 5. 🍜 探索台中特色美食餐廳
      ╰──────────────────────────────────────────────────╯
```

---

## 各功能說明

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

### [功能名稱]（負責：姓名）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

### [功能名稱]（負責：姓名）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

### Skill：[Skill 名稱]（負責：姓名）

- **組合了哪些 Tool**：
- **執行順序**：

```
Step 1: 呼叫 ___ → 取得 ___
Step 2: 呼叫 ___ → 取得 ___
Step 3: 組合輸出 → 產生 ___
```

---

## 心得

### 遇到最難的問題

> 我忘記改gemini調用的版本，一直和我說我額度沒了，差點害我嚇死

### Tool 和 Skill 的差別

> Tool是一個單一功能的函式，skill是多個 Tool 組合起來的工作流程

### 如果再加一個功能

> 可能再加入地圖和規劃路線吧，剛好配合天氣！
