"""
Joke Tool — 取得一則隨機笑話（每日一笑也是健康）
使用 icanhazdadjoke API: https://icanhazdadjoke.com/
翻譯使用 MyMemory Translation API: https://api.mymemory.translated.net
"""

import requests


def _translate_to_zh(text: str) -> str:
    """使用 MyMemory Translation API 將英文翻譯為繁體中文。"""
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": "en|zh-TW"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        translated = data["responseData"]["translatedText"]
        return translated
    except Exception:
        return ""


def get_joke() -> dict:
    """呼叫 icanhazdadjoke API，回傳一則隨機笑話（含中文翻譯）。"""
    try:
        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        joke_text = data["joke"]

        # 翻譯成中文
        joke_zh = _translate_to_zh(joke_text)

        result = {"status": "success", "joke": joke_text}
        if joke_zh:
            result["joke_zh"] = joke_zh
        return result
    except requests.RequestException as e:
        return {"status": "error", "message": f"無法取得笑話：{e}"}


# Gemini Function Declaration
JOKE_TOOL = {
    "name": "get_joke",
    "description": "取得一則隨機英文笑話（Dad Joke）並附上中文翻譯，來自 icanhazdadjoke API。適合為每日計畫加入幽默元素，每日一笑有益健康。",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


if __name__ == "__main__":
    result = get_joke()
    if result["status"] == "success":
        print(f"😂 今日笑話：{result['joke']}")
        if "joke_zh" in result:
            print(f"🀄 中文翻譯：{result['joke_zh']}")
    else:
        print(f"❌ {result['message']}")
