
import urllib.request
import json
import ssl

def get_fun_fact(*args, **kwargs) -> str:
    """取得一則隨機趣味冷知識。"""
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return f"💡 趣味冷知識：{data.get('text', '找不到冷知識')}"
    except Exception as e:
        return f"❌ 取得冷知識失敗: {e}"

# Tool 定義 (供 Agent 使用)
TOOL = {
    "name": "get_fun_fact",
    "description": "取得一則趣味冷知識（讓健康計畫更有趣）。不需要任何參數。",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    }
}

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # 測試執行 Tool
    print("正在測試 get_fun_fact 工具...\n")
    result = get_fun_fact()
    print("輸出結果:")
    print(result)
    print("\nTool 結構確認:")
    print(json.dumps(TOOL, indent=2, ensure_ascii=False))
