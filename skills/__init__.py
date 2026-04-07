"""
Skills 模組 — 組合多個 Tool 的高階技能
每個 Skill 可被 Gemini 自動呼叫，根據使用者意圖判斷。
"""

from .life_advisor_skill import plan_my_day


# ── Gemini Function Declaration（讓 Gemini 自動判斷何時呼叫）────────
PLAN_MY_DAY_DECLARATION = {
    "name": "plan_my_day",
    "description": (
        "為使用者規劃今日生活計畫。會自動取得人生建議，"
        "並組合成包含早中晚行程的完整一日計畫。"
        "適合使用者詢問：今天做什麼、幫我規劃、生活計畫、今日安排等。"
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

# ── Skill 函數映射（供 Agent 調度器使用）──────────────────────────
SKILL_FUNCTIONS = {
    "plan_my_day": plan_my_day,
}

# ── 所有 Skill 的 Gemini Function Declarations ───────────────────
SKILL_DECLARATIONS = [PLAN_MY_DAY_DECLARATION]
