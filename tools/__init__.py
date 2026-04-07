from .weather_tool import get_weather, WEATHER_TOOL_DECLARATION
from .advice_tool import get_advice, ADVICE_TOOL
from .joke_tool import get_joke, JOKE_TOOL
from .fun_fact_tool import get_fun_fact, TOOL as FUN_FACT_TOOL

# 所有工具函數映射（供 Agent 調用）
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "get_advice": get_advice,
    "get_joke": get_joke,
    "get_fun_fact": get_fun_fact,
}

# 所有工具的 Gemini Function Declarations
TOOL_DECLARATIONS = [WEATHER_TOOL_DECLARATION, ADVICE_TOOL, JOKE_TOOL, FUN_FACT_TOOL]
