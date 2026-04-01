# w6-agent--6-

# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題： 旅遊前哨站 /  偵探事務所 /  生活顧問

---

## Agent 功能總覽

> 說明這個 Agent 能做什麼，使用者可以輸入哪些指令

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| （例：天氣） | 呼叫 weather_tool，查詢即時天氣        |          |
| （例：景點） | 呼叫 search_tool，搜尋熱門景點         |          |
| （例：建議） | 呼叫 advice_tool，取得隨機建議         | 林伽紜    |
| （例：出發） | 執行 trip_briefing Skill，產出行前簡報 |          |

---

## 組員與分工

| 姓名 | 負責功能     | 檔案        | 使用的 API |
| ---- | ------------ | ----------- | ---------- |
| 林伽紜 |  取得一則今日人生建議  | `tools/feature/advice-tool`  |  https://api.adviceslip.com/advice  |
|      |              | `tools/`  |            |
|      |              | `tools/`  |            |
|      | Skill 整合   | `skills/` | —         |
|      | Agent 主程式 | `main.py` | —         |

---

## 專案架構

範例：

```
├── tools/
│   ├── advice_tool.py   
│   ├── xxx_tool.py   
│   └── xxx_tool.py  
├── skills/
│   └── xxx_skill.py  
├── main.py        
├── requirements.txt
└── README.md
```

---

## 使用方式

範例：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 執行結果

> 貼上程式執行的實際範例輸出

```
╔═════════════════════════════════════╗
║   🌿 健康生活顧問 Agent 已啟動 🌿       ║
╠═════════════════════════════════════╣
║  試試看輸入「幫我規劃今天」             ║
║  輸入 quit 離開                      ║
╚═════════════════════════════════════╝

你：建議

  🔧 呼叫工具：get_advice
  📥 傳入參數：{}
  📤 回傳結果：{'status': 'success', 'advice': "It's always the quiet ones."}
🤖 顧問：今日人生建議：沈默的人往往最深不可測。
```

---

## 各功能說明

### [今日人生建議]（負責：林伽紜）

- **Tool 名稱**：feature/advice-tool
- **使用 API**：https://api.adviceslip.com/advice
- **輸入**：建議
- **輸出範例**：🤖 顧問：今日人生建議：沈默的人往往最深不可測。

```python
TOOL = {
    "name": "",
    "description": "",
    "parameters": { ... }
}
```

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

> 最大的困難是 Gemini chat.send_message() 回傳 function response 時格式要求與文件不同，需改用 types.Part 直接傳遞而非包在 types.Content 裡，花了一些時間除錯才解決。

### Tool 和 Skill 的差別

> 用自己的話說說，做完後你怎麼理解兩者的不同

### 如果再加一個功能

> 如果可以多加一個 Tool，你會加什麼？為什麼？
