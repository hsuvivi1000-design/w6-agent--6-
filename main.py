"""
健康生活顧問 Agent
使用 Gemini API 建立互動式 Agent，整合 Advice Tool 提供每日生活建議。
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import TOOL_FUNCTIONS, TOOL_DECLARATIONS

# ── 設定 ──────────────────────────────────────────────
MODEL_ID = "gemini-3.1-flash-lite-preview"

SYSTEM_INSTRUCTION = """你是一位貼心的健康生活顧問 Agent。

當使用者要求建議或規劃時，使用 get_advice 工具取得一則建議，然後用一句簡短的繁體中文回覆即可。保持簡潔，不要長篇大論。
"""


def handle_tool_call(tool_name: str, tool_args: dict) -> str:
    """處理工具呼叫，回傳結果字串。"""
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return f"錯誤：找不到工具 {tool_name}"

    print(f"  🔧 呼叫工具：{tool_name}")
    print(f"  📥 傳入參數：{tool_args}")

    result = func(**tool_args) if tool_args else func()

    print(f"  📤 回傳結果：{result}")
    return str(result)


def main():
    # ── 載入 .env ──────────────────────────────────────
    load_dotenv()

    # ── 初始化 Gemini Client ────────────────────────────
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 請先設定環境變數 GEMINI_API_KEY")
        print("   export GEMINI_API_KEY='your-api-key'")
        return

    client = genai.Client(api_key=api_key)

    # ── 建立 Tool 定義 ─────────────────────────────────
    tools = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(**decl) for decl in TOOL_DECLARATIONS
        ]
    )

    # ── 建立對話 ───────────────────────────────────────
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[tools],
    )

    chat = client.chats.create(model=MODEL_ID, config=config)

    print("╔══════════════════════════════════════╗")
    print("║   🌿 健康生活顧問 Agent 已啟動 🌿     ║")
    print("╠══════════════════════════════════════╣")
    print("║  試試看輸入「幫我規劃今天」          ║")
    print("║  輸入 quit 離開                      ║")
    print("╚══════════════════════════════════════╝")
    print()

    # ── 對話迴圈 ───────────────────────────────────────
    while True:
        user_input = input("你：").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("👋 再見！祝你有美好的一天！")
            break

        print()

        # 發送訊息給模型
        response = chat.send_message(user_input)

        # 處理工具呼叫迴圈
        while response.candidates[0].content.parts:
            has_function_call = False

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_function_call = True
                    fc = part.function_call

                    # 呼叫對應工具
                    result_str = handle_tool_call(
                        fc.name, dict(fc.args) if fc.args else {}
                    )

                    # 將結果回傳給模型
                    response = chat.send_message(
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=fc.name,
                                response={"result": result_str},
                            )
                        )
                    )
                    break  # 重新檢查新回覆

            if not has_function_call:
                break

        # 印出最終回覆
        final_text = response.candidates[0].content.parts[0].text
        print(f"🤖 顧問：{final_text}")
        print()


if __name__ == "__main__":
    main()
