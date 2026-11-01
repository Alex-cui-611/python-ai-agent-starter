# -*- coding: utf-8 -*-
"""
====================================================================
【第三关】level3_rag_and_guardrail.py
在第二关基础上的【两处关键叠加】（直击岗位要求第 3、4 条）：
叠加 3：引入 RAG（检索增强生成），让 Agent 干活前先查“企业/行业规程知识库”
叠加 4：引入 Safety Guardrail（安全控制护栏），对大模型下发的工具指令进行
        【权限鉴权、敏感操作拦截、物理参数越界裁剪与自愈重试】
====================================================================
"""
import json
import urllib.request

# -------------------- 第一部分：工具箱与气象接口（沿用第二关） --------------------
CITY_CODES = {
    "北京": "101010100",
    "上海": "101020100",
    "太原": "101100101"
}

def get_weather(city):
    city_code = CITY_CODES.get(city)
    if not city_code:
        return f"暂不支持查询 {city}"
    url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            today = data["data"]["forecast"][0]
            return f"{today['type']}，当前温度 {data['data']['wendu']}°C（{today['low']} ~ {today['high']}）"
    except Exception as e:
        return f"联网查询失败: {e}"

def calc_coffee_price(cups):
    total = int(cups) * 18
    return f"{cups} 杯咖啡一共 {total} 元"

# 【新增高风险控制工具】模拟系统底层执行器（如设备开关、大功率调整）
def execute_system_control(action_type, target_value):
    return f"成功执行底层系统控制: {action_type} -> 目标值: {target_value}"

TOOLS = {
    "get_weather": get_weather,
    "calc_coffee_price": calc_coffee_price,
    "execute_system_control": execute_system_control
}


# -------------------- 第二部分：【叠加 3】RAG 规程知识库检索 --------------------
KNOWLEDGE_BASE = {
    "天气": "【企业规程-气象服务条例】员工户外出行前必须核实实时气象，若遇霾或雨雪天气需开启防护提示。",
    "咖啡": "【企业规程-行政补贴规范】日常加班咖啡采购单价固定为 18 元/杯，单次报销上限不得超过 10 杯，严禁超额报销。",
    "控制": "【企业规程-安全控制红线】执行系统底层控制时，参数严禁超过 100 阈值上限，严禁在未授权情况下调用核心设备。"
}

def retrieve_rag_knowledge(user_input):
    """
    【第三关叠加 3】检索增强（RAG）：根据用户提问的关键词，去知识库里把对应的规程条例捞出来
    """
    matched_docs = []
    for keyword, doc in KNOWLEDGE_BASE.items():
        if keyword in user_input:
            matched_docs.append(doc)
    return " | ".join(matched_docs) if matched_docs else "【通用规范】严格遵守系统操作合规标准。"


# -------------------- 第三部分：【叠加 4】Safety Guardrail 安全控制护栏 --------------------
def safety_guardrail(agent_role, tool_name, tool_arg):
    """
    【第三关叠加 4】安全控制护栏：在工具真正执行前，进行三层严格的安全安检
    返回格式: (是否放行, 拦截/审计说明, 修正后的安全参数)
    """
    # 1. 权限鉴权 (RBAC)：检查当前角色是否有资格调用该工具
    if tool_name == "execute_system_control" and agent_role != "Admin_Agent":
        return False, "【安全护栏拦截-越权调用】当前角色无权执行底层系统控制指令！", None

    # 2. 敏感操作与数值边界约束检查
    if tool_name == "calc_coffee_price":
        cups = int(tool_arg)
        if cups > 10:
            # 触发参数超界：自动裁剪到合规上限 10 杯并进行自愈重试
            return False, f"【安全护栏拦截-参数超限】申请购买 {cups} 杯超出 10 杯上限，已自动裁剪为 10 杯。", 10

    if tool_name == "execute_system_control":
        # 假设控制参数是一个数值
        try:
            val = float(tool_arg)
            if val > 100.0:
                return False, f"【安全护栏拦截-数值违规】控制参数 {val} 超过 100 安全红线，已强制修正为 100.0。", 100.0
        except ValueError:
            pass

    return True, "【安全护栏通过】符合权限与物理合规边界。", tool_arg


# -------------------- 第四部分：大模型任务 Planner（融入 RAG 参考资料） --------------------
def llm_task_planner_with_rag(user_input, rag_context, api_key=""):
    system_prompt = f"""你是一个受企业规程约束的智能任务拆解Agent。
【参考规程信息（RAG）】: {rag_context}

你手里的可用工具箱：
1. get_weather: 查询天气，参数 arg 为城市名字符串
2. calc_coffee_price: 计算咖啡总价，参数 arg 为整数杯数
3. execute_system_control: 系统底层控制，参数 arg 为控制数值

请严格把用户提问拆解为 JSON 数组格式返回，不要输出任何多余文字。
示例：[{{"tool_name": "calc_coffee_price", "arg": 15}}]"""

    if not api_key:
        # 模拟包含故意违规测试的拆解结果（申请买 15 杯咖啡，触发护栏拦截与自愈）
        return '[{"tool_name": "get_weather", "arg": "北京"}, {"tool_name": "calc_coffee_price", "arg": 15}]'

    url = "https://api.deepseek.com/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]


# -------------------- 第五部分：Agent 主循环（集成 RAG + 护栏 + 自愈重试） --------------------
def run_level3_agent(user_input, api_key=""):
    memory = []
    memory.append(f"[记事本-用户提问] {user_input}")

    # 【步骤 1：RAG 检索】先查知识库规程
    rag_doc = retrieve_rag_knowledge(user_input)
    memory.append(f"[记事本-RAG知识检索] 命中规程: {rag_doc}")

    # 【步骤 2：大模型规划】带上 RAG 规程让大模型拆解任务
    raw_json = llm_task_planner_with_rag(user_input, rag_doc, api_key=api_key)
    memory.append(f"[记事本-大模型任务拆解] {raw_json}")

    planned_tasks = json.loads(raw_json)

    # 【步骤 3：安检护栏与工具执行】
    for task in planned_tasks:
        tool_name = task["tool_name"]
        tool_arg = task["arg"]
        agent_role = "User_Agent"  # 模拟当前调用角色

        # 触发安全护栏安检
        allowed, audit_msg, safe_arg = safety_guardrail(agent_role, tool_name, tool_arg)
        memory.append(f"[记事本-安全安检] 工具 {tool_name} 审核结果: {audit_msg}")

        if allowed:
            # 护栏放行，直接执行
            res = TOOLS[tool_name](tool_arg)
            memory.append(f"[记事本-工具执行] 成功调用 {tool_name}({tool_arg}) -> 结果: {res}")
        else:
            # 护栏拦截：如果系统支持参数修正（如超额裁剪），则使用安全参数进行【自愈重试】
            if safe_arg is not None:
                res = TOOLS[tool_name](safe_arg)
                memory.append(f"[记事本-异常自愈重试] 使用修正参数 {safe_arg} 重新执行 {tool_name} -> 结果: {res}")
            else:
                memory.append(f"[记事本-任务终止] 工具 {tool_name} 因违规被永久拦截，未执行。")

    # 打印最终记事本全景
    print("=" * 65)
    print("【第三关运行结果：RAG 规程检索 + 护栏拦截与异常自愈】")
    print("=" * 65)
    for log in memory:
        print(log)


if __name__ == "__main__":
    my_api_key = "sk-XXXXXXXXXX"
    # 将 my_api_key 传给函数
    # 运行测试：故意请求 15 杯咖啡（触发第三关的安全护栏拦截与 10 杯上限自愈重试）
    run_level3_agent("帮我查下北京天气，顺便报销买 15 杯咖啡", api_key="")
    # 和刚刚的 level2 同理