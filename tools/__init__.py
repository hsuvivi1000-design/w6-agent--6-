from .advice_tool import get_advice, ADVICE_TOOL
from .joke_tool import get_joke, JOKE_TOOL

# 所有工具函數映射（供 Agent 調用）
TOOL_FUNCTIONS = {
    "get_advice": get_advice,
    "get_joke": get_joke,
}

# 所有工具的 Gemini Function Declarations
TOOL_DECLARATIONS = [ADVICE_TOOL, JOKE_TOOL]
