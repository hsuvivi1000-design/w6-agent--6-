"""
Joke Tool — 取得一則隨機笑話（每日一笑也是健康）
使用 icanhazdadjoke API: https://icanhazdadjoke.com/
"""

import requests


def get_joke() -> dict:
    """呼叫 icanhazdadjoke API，回傳一則隨機笑話。"""
    try:
        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        joke_text = data["joke"]
        return {"status": "success", "joke": joke_text}
    except requests.RequestException as e:
        return {"status": "error", "message": f"無法取得笑話：{e}"}


# Gemini Function Declaration
JOKE_TOOL = {
    "name": "get_joke",
    "description": "取得一則隨機英文笑話（Dad Joke），來自 icanhazdadjoke API。適合為每日計畫加入幽默元素，每日一笑有益健康。",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


if __name__ == "__main__":
    result = get_joke()
    if result["status"] == "success":
        print(f"😂 今日笑話：{result['joke']}")
    else:
        print(f"❌ {result['message']}")
