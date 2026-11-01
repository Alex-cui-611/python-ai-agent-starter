# -*- coding: utf-8 -*-
"""
====================================================================
【第二关】level2_http_and_llm.py
在第一关基础上的【两处叠加升级】（直接对应岗位任职资格第 2、3 条）：
叠加 1：把第一关的“假天气字典”升级为【真实 HTTP 联网天气接口 + JSON 数据解析】
叠加 2：把第一关写死的 if 拆解升级为【大模型 JSON 结构化任务拆解（支持真实 API 接入）】
====================================================================
"""
import json
import urllib.request

# 常用城市国家气象局代码表
CITY_CODES = {
    "北京": "101010100",
    "上海": "101020100",
    "太原": "101100101",
    "保定": "101090201"  # 雄安新区周边参考气象站
}

# -------------------- 第一部分：升级后的工具箱（真实 HTTP 联网调用） --------------------
def get_weather(city):
    """
    【第二关叠加升级 1】通过 HTTP 接口实时联网查询真实天气，并解析返回的 JSON 结构化数据
    """
    city_code = CITY_CODES.get(city)
    if not city_code:
        return f"暂不支持查询 {city}"

    url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
    try:
        # 发起真实 HTTP GET 请求
        with urllib.request.urlopen(url, timeout=5) as response:
            raw_json_str = response.read().decode("utf-8")
            # 将气象服务器返回的 JSON 字符串解析为 Python 字典
            data = json.loads(raw_json_str)

            today = data["data"]["forecast"][0]
            weather_type = today["type"]       # 天气状况（如：晴、多云）
            low_temp = today["low"]            # 最低温
            high_temp = today["high"]          # 最高温
            curr_temp = data["data"]["wendu"]  # 当前实时温度
            return f"[真实联网数据] {city}今日{weather_type}，当前实时温度 {curr_temp}°C（{low_temp} ~ {high_temp}）"
    except Exception as e:
        return f"联网查询失败（请检查电脑网络）: {e}"


def calc_coffee_price(cups):
    """工具 2：计算买咖啡的总价（保持不变）"""
    total = int(cups) * 18
    return f"{int(cups)} 杯咖啡一共 {total} 元"


TOOLS = {
    "get_weather": get_weather,
    "calc_coffee_price": calc_coffee_price
}


# -------------------- 第二部分：大模型任务拆解器（HTTP POST + JSON 解析） --------------------
SYSTEM_PROMPT = """你是一个任务拆解Agent。你手里有两个工具：
1. get_weather: 查询城市真实天气，参数 arg 为城市名字符串（如 "北京"、"太原"）
2. calc_coffee_price: 计算咖啡总价，参数 arg 为整数杯数（如 5）

请严格把用户的提问拆解为 JSON 数组格式输出，不要输出任何额外解释或 Markdown 标记。
输出示例：[{"tool_name": "get_weather", "arg": "北京"}, {"tool_name": "calc_coffee_price", "arg": 5}]"""


def llm_task_planner(user_input, api_key=""):
    """
    【第二关叠加升级 2】让大模型阅读用户提问，返回标准的 JSON 任务列表字符串
    - 如果你还没有填 api_key，默认返回一段标准的大模型 JSON 响应文本，保证代码直接能跑通
    - 如果你填入了免费的 DeepSeek API Key，则会向大模型服务器发送真实的 HTTP POST 请求
    """
    if not api_key:
        print("💡 [提示] 当前未填写大模型 API_KEY，使用标准 JSON 模拟大模型拆解输出...")
        return '[{"tool_name": "get_weather", "arg": "北京"}, {"tool_name": "get_weather", "arg": "太原"}, {"tool_name": "calc_coffee_price", "arg": 5}]'

    # 真实调用大模型 HTTP 接口
    url = "https://api.deepseek.com/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp_dict = json.loads(resp.read().decode("utf-8"))
        return resp_dict["choices"][0]["message"]["content"]


# -------------------- 第三部分：Agent 主循环（与第一关结构一脉相承） --------------------
def run_level2_agent(user_input, api_key=""):
    memory = []
    memory.append(f"[记事本-用户提问] {user_input}")

    # 【第 2 步升级】：不再用写死的 if，而是拿到 JSON 字符串并用 json.loads() 解析为 Python 列表
    raw_json_response = llm_task_planner(user_input, api_key=api_key)
    memory.append(f"[记事本-大模型原始JSON输出] {raw_json_response}")

    planned_tasks = json.loads(raw_json_response)

    # 【第 3 步：动手执行工具】（这几行代码和第一关一模一样！）
    for task in planned_tasks:
        tool_name = task["tool_name"]
        tool_arg = task["arg"]

        tool_func = TOOLS[tool_name]
        result = tool_func(tool_arg)
        memory.append(f"[记事本-工具执行] 调用 {tool_name}({tool_arg}) -> 返回结果: {result}")

    # 【第 4 步：打印完整执行日志】
    print("=" * 60)
    print("【第二关运行结果：HTTP 实时联网接口 + JSON 结构化任务拆解】")
    print("=" * 60)
    for log in memory:
        print(log)


if __name__ == "__main__":
    #如需测试真实 API，可将你的 Key 填入脚本底部
    my_api_key = "sk-XXXXXXXXXX"
    # 将 my_api_key 传给函数,
    run_level2_agent("帮我查下今天北京和太原的真实天气，再算一下买 5 杯咖啡多少钱", api_key="")
    # 当测试真实API时候，将 api_key=""改为 api_key=my_api_key