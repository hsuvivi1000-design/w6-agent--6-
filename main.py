"""
🤖 Gemini AI Agent — 天氣生活顧問
===================================
使用 Gemini API 的 Function Calling 功能，
搭配 wttr.in 天氣工具，查詢天氣並推薦適合的活動。
"""

import os
import json
import time
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

# 從 tools 資料夾匯入天氣工具
from tools.weather_tool import WEATHER_TOOL_DECLARATION, get_weather

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
║          🌤️  天氣生活顧問 AI Agent  🌤️              ║
║                                                      ║
║   查詢任何城市的天氣，AI 幫你決定今天適合做什麼！    ║
║   輸入 'quit' 或 'exit' 離開                         ║
╚══════════════════════════════════════════════════════╝
{Color.RESET}"""
    print(banner)


def print_step(icon: str, title: str, content: str = "", color: str = Color.CYAN):
    """格式化印出每個步驟"""
    print(f"\n{color}{Color.BOLD}  {icon}  {title}{Color.RESET}")
    if content:
        for line in content.strip().split("\n"):
            print(f"  {Color.DIM}    │ {line}{Color.RESET}")
    print()


# ── 工具分派器 ───────────────────────────────────────────────────
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
}


def handle_tool_call(function_call) -> str:
    """
    根據 Gemini 回傳的 function_call 執行對應工具，
    並在終端機顯示完整的呼叫過程。
    """
    name = function_call.name
    args = dict(function_call.args) if function_call.args else {}

    # 顯示 Agent 決定呼叫工具
    print_step(
        "🔧", 
        f"Agent 決定呼叫工具: {name}",
        f"參數: {json.dumps(args, ensure_ascii=False, indent=2)}",
        Color.YELLOW,
    )

    # 執行工具
    if name in TOOL_FUNCTIONS:
        result = TOOL_FUNCTIONS[name](**args)
    else:
        result = {"error": f"未知的工具: {name}"}

    result_str = json.dumps(result, ensure_ascii=False, indent=2)

    # 顯示工具回傳結果
    print_step(
        "📊",
        f"工具回傳結果 ({name})",
        result_str,
        Color.GREEN,
    )

    return result_str


# ── Gemini API 呼叫（含重試）────────────────────────────────────
def call_gemini(client, chat_history, system_instruction, weather_tool, max_retries=3):
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
                    tools=[weather_tool],
                    temperature=0.7,
                ),
            )
            return response
        except genai_errors.ClientError as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                # 嘗試從錯誤訊息中解析等待秒數
                wait_match = re.search(r'retry.*?(\d+)', error_msg, re.IGNORECASE)
                wait_sec = int(wait_match.group(1)) if wait_match else 30
                wait_sec = min(wait_sec, 60)  # 最多等 60 秒

                if attempt < max_retries:
                    print_step(
                        "⏳",
                        f"API 配額限制 (第 {attempt}/{max_retries} 次重試)",
                        f"等待 {wait_sec} 秒後自動重試...",
                        Color.YELLOW,
                    )
                    time.sleep(wait_sec)
                else:
                    print_step(
                        "❌",
                        "API 配額已耗盡",
                        "已重試 {0} 次仍失敗。\n"
                        "建議：\n"
                        "  1. 等幾分鐘後再試\n"
                        "  2. 到 https://aistudio.google.com/apikey 換一組新的 API Key\n"
                        "  3. 確認你的 Gemini API 方案配額".format(max_retries),
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
      使用者輸入 → Gemini 判斷 → (呼叫工具 → 回傳結果 →) 最終回覆
    """

    # Step 1: 顯示使用者輸入
    print_step("👤", "使用者輸入", user_input, Color.BLUE)

    # Step 2: 將使用者訊息加入歷史
    chat_history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)],
    ))

    # Step 3: 呼叫 Gemini API
    print_step("🤖", "正在思考中...", "將訊息送給 Gemini API", Color.CYAN)

    # 定義工具
    weather_tool = types.Tool(function_declarations=[WEATHER_TOOL_DECLARATION])

    # 系統提示
    system_instruction = types.Content(
        parts=[types.Part.from_text(text=(
            "你是一個天氣生活顧問 AI。當使用者詢問天氣或活動建議時，"
            "請使用 get_weather 工具查詢天氣資訊。\n\n"
            "取得天氣資訊後，請根據以下規則給出建議：\n"
            "1. 根據溫度、降雨機率、風速等判斷適合室內還是室外活動\n"
            "2. 根據天氣描述決定具體的活動類型\n"
            "3. 給出 3-5 個具體的活動建議\n"
            "4. 使用 emoji 讓回覆更生動\n\n"
            "判斷標準：\n"
            "- 降雨機率 > 60% → 推薦室內活動\n"
            "- 溫度 > 35°C 或 < 5°C → 推薦室內活動\n"
            "- 風速 > 40 km/h → 推薦室內活動\n"
            "- 其他情況 → 推薦室外活動\n\n"
            "回覆格式：先總結天氣狀況，再給出室內/室外判定，最後列出活動建議。"
        ))]
    )

    response = call_gemini(client, chat_history, system_instruction, weather_tool)
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

                # 執行工具
                result_str = handle_tool_call(part.function_call)

                # 將工具結果加入歷史
                print_step("🔄", "將工具結果回傳給 Gemini...", "", Color.CYAN)

                chat_history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=part.function_call.name,
                        response=json.loads(result_str),
                    )],
                ))

                # 再次呼叫 Gemini，讓它根據工具結果生成回覆
                response = call_gemini(client, chat_history, system_instruction, weather_tool)
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
