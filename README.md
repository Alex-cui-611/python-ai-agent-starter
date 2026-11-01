# 🤖 Python AI Agent 实战：从零构建智能体工作流 (4-Levels Starter)

本项目是一个面向初学者的 Python AI Agent（智能体）实战演练库。通过四个层层递进的 Python 脚本，带你从零理解并实现大模型（LLM）与传统代码、外部 API、企业级规程知识库（RAG）及多智能体协作与自动化评测的深度融合。

---

## 📂 项目结构与关卡设计

| 关卡文件 | 核心技术与应用场景 | 对应核心知识点 |
| :--- | :--- | :--- |
| **`level1_basic_loop.py`** | **基础循环与上下文记忆** | • 记事本机制（Memory）<br>• 基础任务拆解（Planner）<br>• 工具箱映射与调用（Tool Execution） |
| **`level2_http_and_llm.py`** | **联网接口与大模型动态调用** | • 真实 HTTP GET/POST 请求<br>• JSON 结构化数据解析<br>• 大模型 API 提示词工程与意图识别 |
| **`level3_rag_and_guardrail.py`** | **RAG 知识检索与安全护栏** | • 检索增强生成（RAG 规程检索）<br>• 安全控制护栏（Safety Guardrail）<br>• 敏感操作拦截、超限裁剪与异常自愈 |
| **`level4_multi_agent_benchmark.py`** | **多智能体协作与自动化评测** | • 多智能体分工流（Orchestrator）<br>• 自动化评测基准（Benchmark Suite）<br>• 综合防御成功率、时延与量化统计 |

---

## 🚀 各关卡详细介绍与学习笔记

### Level 1：Agent 的核心工作循环 (`level1_basic_loop.py`)
* **核心思想**：大模型本质上是一个“只会动嘴的聪明大脑”，而 Agent 是通过“记事本 + 双手”让它动起来。
* **实现逻辑**：
  1. 使用 Python 列表 `memory = []` 记录用户提问与每一步操作（上下文记忆）。
  2. 使用 `TOOLS` 字典将字符串名字映射为真正的 Python 函数。
  3. 模拟任务拆解与循环执行，理解 Agent 最基础的 **Input ➔ Think ➔ Act ➔ Output** 闭环。

### Level 2：真实联网与大模型 API 对接 (`level2_http_and_llm.py`)
* **核心思想**：摆脱本地写死的假数据，让大模型真正“看懂人话”并发起网络请求。
* **实现逻辑**：
  1. 编写 `get_weather` 函数，通过 `urllib.request` 实时向公开气象接口发起 HTTP 请求，拉取实时天气。
  2. 编写 `llm_task_planner` 函数，将自然语言请求发送给大模型 API（如 DeepSeek），让大模型动态输出标准的 **JSON 结构化指令**。
  3. 用 `json.loads()` 将大模型返回的文本解析为 Python 列表并自动驱动工具执行。

### Level 3：企业级 RAG 与安全护栏 (`level3_rag_and_guardrail.py`)
* **核心思想**：解决大模型的“幻觉”与“盲目瞎跑”问题，增加企业规程约束与安全防线。
* **实现逻辑**：
  1. **RAG 检索增强**：在大模型思考前，先去本地知识库 `KNOWLEDGE_BASE` 中检索相关的政策/规程，作为“开卷考试”的参考资料喂给模型。
  2. **Safety Guardrail（安全护栏）**：在工具真正执行前加入严密的 `if-else` 安检：
     * **权限鉴权 (RBAC)**：防止普通用户越权调用高风险系统控制接口。
     * **参数超限自愈**：当申请购买超过上限的咖啡时，自动触发裁剪并进行自愈重试。

### Level 4：多智能体协作与量化评测 (`level4_multi_agent_benchmark.py`)
* **核心思想**：从单个脚本走向工程化、系统化评测。
* **实现逻辑**：
  1. **多智能体分工**：通过 `MultiAgentOrchestrator` 调度器，将任务流解耦为规划、安检、执行等多角色协作。
  2. **自动化评测基准 (Benchmark Suite)**：设计包含正常查询、超限自愈、越权拦截等混合测试集 (`test_suite`)。
  3. 自动统计并输出**系统综合防御与任务成功率、合规执行率、主动拦截次数及平均调度时延**等量化指标。

---

## 🛠️ 如何快速运行本项目

1. **环境准备**：
   本项目完全基于 Python 原生库开发（使用 `json`、`urllib.request`、`time` 等），**无需执行繁琐的 `pip install` 第三方依赖包安装**（对新手极其友好）。

2. **克隆项目并运行**：
   ```bash
   git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
   cd 你的仓库名
   
   # 运行第一关
   python level1_basic_loop.py
   
   # 运行第二关（如需测试真实 API，可将你的 Key 填入脚本底部）
   python level2_http_and_llm.py
   
   # 运行第三关
   python level3_rag_and_guardrail.py
   
   # 运行第四关自动化评测
   python level4_multi_agent_benchmark.py