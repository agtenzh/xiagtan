# AI多代理系统 - 开发文档

## 项目结构

```
agency-ai-system/
├── orchestrator/              # 总控服务
│   ├── app/
│   │   ├── brains/           # 大脑实现
│   │   │   ├── brain_base.py # 大脑基类
│   │   │   └── manager.py    # 大脑管理器
│   │   ├── agents/           # 代理实现
│   │   │   ├── agent_base.py # 代理基类
│   │   │   ├── marketing_agents.py
│   │   │   ├── development_agents.py
│   │   │   ├── design_agents.py
│   │   │   ├── sales_agents.py
│   │   │   └── manager.py
│   │   ├── api/              # API路由
│   │   │   ├── routes.py
│   │   │   ├── audit_routes.py
│   │   │   ├── heartbeat_routes.py
│   │   │   └── progress_routes.py
│   │   ├── core/             # 核心逻辑
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── logging.py
│   │   │   └── adaptive_config.py
│   │   ├── models/           # 数据模型
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   └── audit_log.py
│   │   ├── services/         # 业务服务
│   │   │   ├── audit_service.py
│   │   │   ├── heartbeat_service.py
│   │   │   ├── progress_monitor.py
│   │   │   └── message_queue.py
│   │   └── utils/            # 工具函数
│   │       └── health_check.py
│   ├── tests/                # 测试文件
│   │   ├── conftest.py
│   │   ├── test_brain.py
│   │   ├── test_agent.py
│   │   └── test_api.py
│   ├── config/
│   ├── data/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── agent-worker/              # 代理池服务
├── dashboard/                 # 前端界面
│   ├── src/
│   │   ├── components/
│   │   │   ├── MindMap/
│   │   │   ├── Agent/
│   │   │   └── Dashboard/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── api/
│   │   └── router/
│   ├── package.json
│   └── Dockerfile
├── config/                    # 配置文件
├── docs/                      # 文档
├── docker-compose.yml
├── PROGRESS.md
└── README.md
```

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy
- asyncio
- loguru

### 前端
- Vue.js 3
- TypeScript
- Element Plus
- cytoscape.js
- ECharts

### 数据库
- SQLite (低配置)
- PostgreSQL (高配置)
- Redis (缓存)

## 开发指南

### 添加新代理

1. 在 `orchestrator/app/agents/` 创建新文件
2. 继承 `BaseAgent` 基类
3. 实现 `execute` 和 `get_prompt` 方法
4. 在 `manager.py` 中注册代理

```python
from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory

class MyAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="我的代理",
            description="自定义代理",
            category=AgentCategory.DEVELOPMENT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["tool1", "tool2"],
            capabilities=["cap1", "cap2"],
            prompt_template="你是一个专家..."
        )
        super().__init__(config)
    
    def get_prompt(self, task):
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task):
        # 实现执行逻辑
        return {"status": "completed", "output": "结果"}
```

### 添加新大脑

1. 在 `orchestrator/app/brains/brain_base.py` 创建新类
2. 继承 `Brain` 基类
3. 实现 `process_task` 和 `select_agent` 方法
4. 在 `manager.py` 中注册大脑

### 添加新API

1. 在 `orchestrator/app/api/` 创建新路由文件
2. 在 `routes.py` 中注册路由

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/my", tags=["我的API"])

@router.get("/endpoint")
async def my_endpoint():
    return {"message": "Hello"}
```

### 添加新Vue页面

1. 在 `dashboard/src/views/` 创建新页面
2. 在 `router/index.ts` 添加路由
3. 在 `App.vue` 添加菜单项

## 测试

### 运行测试

```bash
cd orchestrator
pytest tests/ -v
```

### 测试覆盖率

```bash
pytest tests/ --cov=app --cov-report=html
```

## 部署

### Docker部署

```bash
docker-compose up -d
```

### 手动部署

```bash
# 后端
cd orchestrator
pip install -r requirements.txt
python main.py

# 前端
cd dashboard
npm install
npm run build
```
