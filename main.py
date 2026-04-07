"""
🤖 Gemini AI Agent — 智慧生活顧問
===================================
使用 Gemini API 的 Function Calling 功能，
搭配多種工具與技能，自動判斷使用者意圖並呼叫對應功能。

支援的工具：
  🌤️ 天氣查詢 (get_weather)
  💡 人生建議 (get_advice)
  😂 隨機笑話 (get_joke)
  🧠 趣味冷知識 (get_fun_fact)

支援的技能：
  🌟 今日生活計畫 (plan_my_day)
"""

import os
import json
import time
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

# ── 從 tools 資料夾匯入所有工具 ───────────────────────────────────
from tools.weather_tool import WEATHER_TOOL_DECLARATION, get_weather
from tools.advice_tool import ADVICE_TOOL, get_advice
from tools.joke_tool import JOKE_TOOL, get_joke
from tools.fun_fact_tool import TOOL as FUN_FACT_TOOL, get_fun_fact

# ── 從 skills 資料夾匯入所有技能 ──────────────────────────────────
from skills import SKILL_FUNCTIONS, SKILL_DECLARATIONS

load_dotenv()

# ── 顏色常數（終端機美化輸出）────────────────────────────────────
class Color:
    HEADER  = "\033[95m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


def print_banner():
    """印出啟動橫幅"""
    banner = f"""
{Color.CYAN}{Color.BOLD}
╔══════════════════════════════════════════════════════╗
║          🤖  智慧生活顧問 AI Agent  🤖              ║
║                                                      ║
║   🌤️ 天氣 │ 💡 建議 │ 😂 笑話 │ 🧠 冷知識          ║
║   🌟 今日生活計畫                                    ║
║                                                      ║
║   Gemini 會自動判斷你的需求，呼叫對應工具！          ║
║   輸入 'quit' 或 'exit' 離開                         ║
╚══════════════════════════════════════════════════════╝
{Color.RESET}"""
    print(banner)

    # 顯示已載入的工具與技能
    print(f"{Color.DIM}  📦 已載入 {len(TOOL_FUNCTIONS)} 個工具 + {len(SKILL_FUNCTIONS)} 個技能{Color.RESET}")
    print(f"{Color.DIM}  🔧 工具: {', '.join(TOOL_FUNCTIONS.keys())}{Color.RESET}")
    print(f"{Color.DIM}  🌟 技能: {', '.join(SKILL_FUNCTIONS.keys())}{Color.RESET}")
    print()


def print_step(icon: str, title: str, content: str = "", color: str = Color.CYAN):
    """格式化印出每個步驟"""
    print(f"\n{color}{Color.BOLD}  {icon}  {title}{Color.RESET}")
    if content:
        for line in content.strip().split("\n"):
            print(f"  {Color.DIM}    │ {line}{Color.RESET}")
    print()


# ── 統一的工具 + 技能函數映射 ─────────────────────────────────────
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "get_advice": get_advice,
    "get_joke": get_joke,
    "get_fun_fact": get_fun_fact,
}

# 將 skill 函數也加入映射（Gemini 可以統一呼叫）
TOOL_FUNCTIONS.update(SKILL_FUNCTIONS)

# ── 統一的 Gemini Function Declarations ───────────────────────────
ALL_DECLARATIONS = [
    WEATHER_TOOL_DECLARATION,
    ADVICE_TOOL,
    JOKE_TOOL,
    FUN_FACT_TOOL,
] + SKILL_DECLARATIONS


def handle_tool_call(function_call) -> str:
    """
    根據 Gemini 回傳的 function_call 執行對應工具或技能，
    並在終端機顯示完整的呼叫過程。
    """
    name = function_call.name
    args = dict(function_call.args) if function_call.args else {}

    # 判斷是工具還是技能
    is_skill = name in SKILL_FUNCTIONS
    label = "技能 (Skill)" if is_skill else "工具 (Tool)"
    icon = "🌟" if is_skill else "🔧"

    # 顯示 Agent 決定呼叫
    print_step(
        icon, 
        f"Agent 決定呼叫{label}: {name}",
        f"參數: {json.dumps(args, ensure_ascii=False, indent=2)}" if args else "（無需參數）",
        Color.YELLOW,
    )

    # 執行工具或技能
    if name in TOOL_FUNCTIONS:
        result = TOOL_FUNCTIONS[name](**args)
    else:
        result = {"error": f"未知的工具/技能: {name}"}

    # 統一轉成字串
    if isinstance(result, str):
        result_str = result
        result_dict = {"result": result}
    elif isinstance(result, dict):
        result_str = json.dumps(result, ensure_ascii=False, indent=2)
        result_dict = result
    else:
        result_str = str(result)
        result_dict = {"result": result_str}

    # 顯示回傳結果
    print_step(
        "📊",
        f"{label}回傳結果 ({name})",
        result_str,
        Color.GREEN,
    )

    return json.dumps(result_dict, ensure_ascii=False) if isinstance(result_dict, dict) else result_str


# ── Gemini API 呼叫（含重試）────────────────────────────────────
def call_gemini(client, chat_history, system_instruction, gemini_tools, max_retries=3):
    """
    呼叫 Gemini API，遇到 429 限流時自動等待並重試。
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=chat_history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[gemini_tools],
                    temperature=0.7,
                ),
            )
            return response
        except genai_errors.ClientError as e:
            error_msg = str(e)
            # 將 429 (資源耗盡) 和 503 (伺服器負載過高) 都加入自動重試機制
            if any(key in error_msg for key in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"]):
                # 嘗試從錯誤訊息中解析等待秒數
                wait_match = re.search(r'retry.*?(\d+)', error_msg, re.IGNORECASE)
                wait_sec = int(wait_match.group(1)) if wait_match else 5  # 找不到等待秒數預設等 5 秒
                wait_sec = min(wait_sec, 60)  # 最多等 60 秒

                if attempt < max_retries:
                    print_step(
                        "⏳",
                        f"伺服器繁忙或配額限制 (第 {attempt}/{max_retries} 次重試)",
                        f"等待 {wait_sec} 秒後自動重試...\n錯誤詳情: {error_msg}",
                        Color.YELLOW,
                    )
                    time.sleep(wait_sec)
                else:
                    print_step(
                        "❌",
                        "伺服器持續繁忙或配額已耗盡",
                        "已重試 {0} 次仍失敗。\n"
                        "建議：\n"
                        "  1. 等幾分鐘後再試\n"
                        "  2. 確認你的 Gemini API 方案配額".format(max_retries),
                        Color.RED,
                    )
                    return None
            else:
                print_step("❌", "API 呼叫失敗", str(e), Color.RED)
                return None
        except Exception as e:
            print_step("❌", "發生未預期的錯誤", str(e), Color.RED)
            return None
    return None


# ── Agent 主邏輯 ─────────────────────────────────────────────────
def run_agent(user_input: str, client, chat_history: list):
    """
    執行一次 Agent 迴圈：
      使用者輸入 → Gemini 判斷 → (自動選擇工具/技能 → 回傳結果 →) 最終回覆
    """

    # Step 1: 顯示使用者輸入
    print_step("👤", "使用者輸入", user_input, Color.BLUE)

    # Step 2: 將使用者訊息加入歷史
    chat_history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)],
    ))

    # Step 3: 呼叫 Gemini API
    print_step("🤖", "正在思考中...", "Gemini 正在分析你的需求，決定使用哪個工具", Color.CYAN)

    # 定義所有可用的工具（tools + skills）
    gemini_tools = types.Tool(function_declarations=ALL_DECLARATIONS)

    # 系統提示 — 告訴 Gemini 所有可用的工具與技能
    system_instruction = types.Content(
        parts=[types.Part.from_text(text=(
            "你是一個智慧生活顧問 AI，具備多種工具和技能。"
            "請根據使用者的輸入，自動判斷應該使用哪個工具或技能。\n\n"
            "你可以使用以下工具：\n"
            "1. get_weather — 查詢天氣：當使用者問天氣、氣溫、下雨等相關問題時使用\n"
            "2. get_advice — 人生建議：當使用者想要建議、激勵、座右銘時使用\n"
            "3. get_joke — 隨機笑話：當使用者想聽笑話、想開心、無聊時使用\n"
            "4. get_fun_fact — 趣味冷知識：當使用者好奇、想學新知識、問冷知識時使用\n\n"
            "你還可以使用以下技能（Skill，組合多個工具的進階功能）：\n"
            "5. plan_my_day — 今日生活計畫：當使用者想規劃今天、問今天做什麼時使用\n\n"
            "判斷規則：\n"
            "- 天氣相關關鍵字（天氣、氣溫、下雨、溫度、城市天氣）→ get_weather\n"
            "- 建議/激勵相關（建議、座右銘、激勵、鼓勵）→ get_advice\n"
            "- 笑話/幽默相關（笑話、搞笑、有趣的、逗我笑）→ get_joke\n"
            "- 冷知識/趣聞（冷知識、有趣的事、你知道嗎、trivia）→ get_fun_fact\n"
            "- 規劃/計畫（規劃今天、今天做什麼、生活計畫、每日安排）→ plan_my_day\n"
            "- 如果不確定，可以直接回覆使用者，不需要呼叫任何工具\n\n"
            "回覆要求：\n"
            "1. 使用繁體中文回覆\n"
            "2. 使用 emoji 讓回覆更生動\n"
            "3. 根據工具回傳的結果給出有用的分析和建議\n"
            "4. 語氣親切友善"
        ))]
    )

    response = call_gemini(client, chat_history, system_instruction, gemini_tools)
    if response is None:
        return None

    # Step 4: 檢查是否需要呼叫工具（可能多輪）
    while response.candidates[0].content.parts:
        has_function_call = False

        for part in response.candidates[0].content.parts:
            if part.function_call:
                has_function_call = True

                # 將 model 的 function_call 回應加入歷史
                chat_history.append(response.candidates[0].content)

                # 執行工具或技能
                result_str = handle_tool_call(part.function_call)

                # 將工具結果加入歷史
                print_step("🔄", "將結果回傳給 Gemini 進行分析...", "", Color.CYAN)

                chat_history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=part.function_call.name,
                        response=json.loads(result_str) if result_str.startswith("{") else {"result": result_str},
                    )],
                ))

                # 再次呼叫 Gemini，讓它根據工具結果生成回覆
                response = call_gemini(client, chat_history, system_instruction, gemini_tools)
                if response is None:
                    return None
                break  # 重新檢查新的 response

        if not has_function_call:
            break

    # Step 5: 取得最終回覆
    final_text = response.text
    chat_history.append(response.candidates[0].content)

    # 顯示最終回覆
    print(f"\n{Color.GREEN}{Color.BOLD}  💬  Agent 最終回覆{Color.RESET}")
    print(f"  {Color.DIM}    ╭{'─' * 50}╮{Color.RESET}")
    for line in final_text.strip().split("\n"):
        print(f"  {Color.DIM}    │{Color.RESET} {line}")
    print(f"  {Color.DIM}    ╰{'─' * 50}╯{Color.RESET}")
    print()

    return final_text


# ── 主程式 ───────────────────────────────────────────────────────
def main():
    # 檢查 API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Color.RED}❌ 錯誤: 請設定 GEMINI_API_KEY 環境變數{Color.RESET}")
        print(f"{Color.DIM}   方式 1: 建立 .env 檔案並寫入 GEMINI_API_KEY=你的金鑰{Color.RESET}")
        print(f"{Color.DIM}   方式 2: set GEMINI_API_KEY=你的金鑰  (Windows){Color.RESET}")
        return

    # 建立 Gemini client
    client = genai.Client(api_key=api_key)

    print_banner()

    # 對話歷史
    chat_history = []

    # 互動迴圈
    while True:
        try:
            user_input = input(f"{Color.BOLD}🗣️  請輸入 ▸ {Color.RESET}").strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "bye", "結束"):
                print(f"\n{Color.CYAN}👋 感謝使用，再見！{Color.RESET}\n")
                break

            run_agent(user_input, client, chat_history)

        except genai_errors.ClientError as e:
            print_step("❌", "API 錯誤", str(e), Color.RED)
            print(f"{Color.YELLOW}  提示: 可以繼續輸入其他問題，或等一下再試。{Color.RESET}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Color.CYAN}👋 感謝使用，再見！{Color.RESET}\n")
            break


if __name__ == "__main__":
    main()
