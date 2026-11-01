# -*- coding: utf-8 -*-
"""
====================================================================
【第一关】level1_basic_loop.py
核心目标：不依赖任何外部网络，看懂 AI Agent 干活的“四步核心循环”：
1. 记事本（上下文记忆 Memory）
2. 动脑拆解任务（Planner）
3. 动手调用工具函数（Tool Execution）
4. 汇总结果输出
====================================================================
"""

# -------------------- 第一部分：打造 Agent 的“双手”（工具函数） --------------------
def get_weather(city):
    """工具 1：查询天气（第一关先用本地字典模拟，第二关升级为真实联网接口）"""
    fake_weather_db = {
        "北京": "晴，22°C（本地模拟数据）",
        "上海": "小雨，19°C（本地模拟数据）",
        "太原": "多云，16°C（本地模拟数据）"
    }
    return fake_weather_db.get(city, f"暂无 {city} 的天气数据")


def calc_coffee_price(cups):
    """工具 2：计算买咖啡的总价（每杯 18 元）"""
    total = int(cups) * 18
    return f"{cups} 杯咖啡一共 {total} 元"


# 把所有工具函数装进一个“工具箱字典”里，方便 Agent 按字符串名字查找并调用
TOOLS = {
    "get_weather": get_weather,
    "calc_coffee_price": calc_coffee_price
}


# -------------------- 第二部分：Agent 的“核心四步循环” --------------------
def run_level1_agent(user_input):
    # 【第 1 步：初始化记事本（上下文管理 Context Memory）】
    # 用一个普通列表把用户的提问和 Agent 每一步的操作都记录下来
    memory = []
    memory.append(f"[记事本-用户提问] {user_input}")

    # 【第 2 步：任务拆解（Task Decomposition）】
    # 第一关先用简单的 if 判断来模拟“大脑拆解任务”（第二关会替换成 JSON 解析与大模型接口）
    planned_tasks = []
    if "北京" in user_input:
        planned_tasks.append({"tool_name": "get_weather", "arg": "北京"})
    if "太原" in user_input:
        planned_tasks.append({"tool_name": "get_weather", "arg": "太原"})
    if "咖啡" in user_input:
        planned_tasks.append({"tool_name": "calc_coffee_price", "arg": 3})

    memory.append(f"[记事本-任务规划] 共拆解出 {len(planned_tasks)} 个待执行子任务: {planned_tasks}")

    # 【第 3 步：动手执行工具（Tool Calling）】
    # 遍历拆解好的任务列表，去 TOOLS 字典里找到对应的 Python 函数并传入参数运行
    for task in planned_tasks:
        tool_name = task["tool_name"]  # 取出工具名字，比如 "get_weather"
        tool_arg = task["arg"]         # 取出参数，比如 "北京"

        tool_func = TOOLS[tool_name]   # 从字典里拿出真正的 Python 函数
        result = tool_func(tool_arg)   # 真正执行函数，拿到返回结果

        memory.append(f"[记事本-工具执行] 调用 {tool_name}({tool_arg}) -> 返回结果: {result}")

    # 【第 4 步：打印记事本，查看 Agent 思考和干活的全过程】
    print("=" * 60)
    print("【第一关运行结果：Agent 基础工作循环】")
    print("=" * 60)
    for log in memory:
        print(log)


if __name__ == "__main__":
    run_level1_agent("帮我查下北京和太原的天气，再算一下买咖啡多少钱")