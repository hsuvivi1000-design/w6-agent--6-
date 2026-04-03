"""
Advice Tool — 取得今日人生建議
使用 Advice Slip API: https://api.adviceslip.com/advice
"""

import requests


def get_advice() -> dict:
    """呼叫 Advice Slip API，回傳一則隨機人生建議。"""
    try:
        response = requests.get(
            "https://api.adviceslip.com/advice",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        advice_text = data["slip"]["advice"]
        return {"status": "success", "advice": advice_text}
    except requests.RequestException as e:
        return {"status": "error", "message": f"無法取得建議：{e}"}


# Gemini Function Declaration
ADVICE_TOOL = {
    "name": "get_advice",
    "description": "取得一則隨機的人生建議（英文），來自 Advice Slip API。適合用來為使用者的每日計畫加入一句激勵語錄。",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}
