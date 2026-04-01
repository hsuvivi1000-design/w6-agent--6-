"""
Life Advisor Skill — 生活顧問技能
組合多個 Tool 的結果，產出今日生活計畫。
"""

from tools.advice_tool import get_advice


def plan_my_day() -> str:
    """
    執行今日生活計畫流程：
    Step 1: 呼叫 get_advice → 取得一則人生建議
    Step 2: 組合輸出 → 產生今日生活計畫文字
    （未來可擴充：加入天氣工具、運動建議工具等）
    """
    # Step 1: 取得人生建議
    advice_result = get_advice()

    if advice_result["status"] == "success":
        advice = advice_result["advice"]
    else:
        advice = "保持正面心態，享受每一天！"

    # Step 2: 組合成生活計畫
    plan = f"""
╔══════════════════════════════════════╗
║        🌟 今日生活計畫 🌟            ║
╚══════════════════════════════════════╝

💡 今日建議：{advice}

📋 建議行程：
  🌅 早上 — 根據建議設定今日目標
  🏃 下午 — 安排適度運動與學習
  🌙 晚上 — 回顧今日成果，放鬆身心

✨ 記住：每一天都是新的開始！
"""
    return plan.strip()


if __name__ == "__main__":
    print(plan_my_day())
