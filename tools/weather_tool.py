"""
天氣查詢工具 - 透過 wttr.in API 取得城市天氣資訊
"""

import requests
import json


# ── Gemini Function Declaration ──────────────────────────────────
WEATHER_TOOL_DECLARATION = {
    "name": "get_weather",
    "description": (
        "取得指定城市的即時天氣資訊，包含溫度、體感溫度、濕度、"
        "天氣描述、風速、降雨機率等。用來判斷適合室內或室外活動。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "要查詢天氣的城市名稱，例如 Taipei、Tokyo、New York",
            }
        },
        "required": ["city"],
    },
}


# ── 實際執行函式 ─────────────────────────────────────────────────
def get_weather(city: str) -> dict:
    """
    透過 wttr.in 取得天氣資訊，回傳結構化 dict。
    """
    url = f"https://wttr.in/{city}?format=j1&lang=zh-tw"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        current = data["current_condition"][0]

        weather_info = {
            "city": city,
            "temperature_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "humidity": current["humidity"],
            "weather_desc": current["lang_zh-tw"][0]["value"] if current.get("lang_zh-tw") else current["weatherDesc"][0]["value"],
            "wind_speed_kmh": current["windspeedKmph"],
            "wind_dir": current["winddir16Point"],
            "uv_index": current["uvIndex"],
            "visibility_km": current["visibility"],
            "pressure_mb": current["pressure"],
            "cloud_cover": current["cloudcover"],
            "precip_mm": current["precipMM"],
        }

        # 如果有今日預報，加入降雨機率
        if "weather" in data and len(data["weather"]) > 0:
            today = data["weather"][0]
            max_chance_of_rain = max(
                int(h.get("chanceofrain", 0)) for h in today.get("hourly", [{}])
            )
            weather_info["chance_of_rain_pct"] = max_chance_of_rain
            weather_info["max_temp_c"] = today["maxtempC"]
            weather_info["min_temp_c"] = today["mintempC"]

        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": f"無法取得天氣資訊: {str(e)}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": f"解析天氣資料失敗: {str(e)}"}
