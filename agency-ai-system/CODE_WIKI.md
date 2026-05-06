# Agency AI System - Code Wiki

## 1. 项目概述

### 1.1 项目简介
Agency AI System 是一个基于 Python 的多代理 AI 系统，支持多个专业大脑协作、40+ 个子代理执行任务、可视化思维导图界面。系统采用微服务架构，包含三个核心服务组成。

### 1.2 主要特性
- **多大脑架构**: 支持多个专业大脑协作处理复杂任务
- **40+ 子代理**: 覆盖营销、开发、设计、销售、分析等领域代理
- **可视化界面**: 思维导图展示大脑和代理关系
- **自适应配置**: 根据服务器配置自动调整系统参数
- **实时监控**: CPU、内存、任务、代理状态监控
- **完整的API接口**: 提供 RESTful API 支持

---

## 2. 项目结构

### 2.1 目录树

```
agency-ai-system/
├── agent-worker/              # 代理工作服务
│   ├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── config/                    # 配置文件目录
│   ├── high_config.yaml
│   ├── low_config.yaml
│   ├── medium_config.yaml
│   └── ultra_config.yaml
├── dashboard/               # 前端管理界面
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── types/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/                  # 文档目录
│   ├── api.md
│   ├── development.md
│   └── user_manual.md
├── orchestrator/          # 总控服务（核心）
│   ├── app/
│   │   ├── agents/        # 代理模块
│   │   ├── api/         # API路由
│   │   ├── brains/      # 大脑模块
│   │   ├── config/      # 配置模块
│   │   ├── core/        # 核心功能
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务服务
│   │   └── utils/       # 工具函数
│   ├── tests/            # 测试文件
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── .gitignore
├── ACCESS_GUIDE.md
├── CHANGELOG.md
├── PROGRESS.md
├── README.md
├── TEST_REPORT.md
└── docker-compose.yml
└── test_all.py
```

### 2.2 核心模块结构

#### 2.2.1 orchestrator（总控服务）

| 模块 | 路径 | 职责 |
|------|------|------|
| 主入口 | main.py | FastAPI应用入口，应用初始化，启动事件 |
| 代理模块 | app/agents/ | 代理基类，具体代理实现，代理管理器 |
| 大脑模块 | app/brains/ | 大脑基类，具体大脑实现，大脑网络管理 |
| API路由 | app/api/ | RESTful API路由定义 |
| 核心功能 | app/core/ | 配置，数据库，日志等核心功能 |
| 数据模型 | app/models/ | SQLAlchemy 数据模型定义 |
| 业务服务 | app/services/ | 心跳服务，审计服务，进度监控服务 |
| 配置 | app/config/ | 代理配置，大脑配置 |

---

## 3. 系统架构

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                       Dashboard                         │
│              (Vue 可视化管理界面)                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                       │
│               (FastAPI 总控服务)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Brain   │  │   Agents    │  │   Services  │  │
│  │  Network    │  │   Manager   │  │             │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────┘
        │                    │
        ▼                    ▼
┌──────────────┐        ┌──────────────┐
│  Database  │        │ Agent Worker│
│ (SQLite/  │        │ (Optional) │
│ PostgreSQL)│        └──────────────┘
└──────────────┘
```

### 3.2 核心组件说明

#### 3.2.1 大脑系统

系统包含以下大脑：

- **主大脑 (Master Brain)**: 全局协调、任务分配、负载均衡、结果整合
- **营销大脑 (Marketing Brain)**: 营销策略、内容创作、社交媒体、增长黑客
- **工程大脑 (Engineering Brain)**: 软件开发、架构设计、代码审查、DevOps
- **设计大脑 (Design Brain)**: UI/UX设计、视觉设计、品牌设计
- **销售大脑 (Sales Brain)**: 销售策略、客户管理、管道分析
- **产品大脑 (Product Brain)**: 产品管理、用户研究、反馈分析
- **测试大脑 (Testing Brain)**: 测试自动化、性能测试、质量保证
- **财务大脑 (Finance Brain)**: 财务分析、预算管理、税务策略
- **项目管理大脑 (Project Management Brain)**: 项目规划、执行监控、风险管理
- **付费媒体大脑 (Paid Media Brain)**: PPC策略、付费社交、广告优化
- **专业大脑 (Specialized Brain)**: 法律、招聘、翻译等专业领域
- **学术大脑 (Academic Brain)**: 历史研究、心理学分析等学术领域
- **游戏开发大脑 (Game Development Brain)**: 游戏设计、关卡设计、叙事设计
- **空间计算大脑 (Spatial Computing Brain)**: XR开发、空间计算、沉浸式体验

#### 3.2.2 代理系统

系统包含 40+ 预配置代理，分布在以下类别：

- 营销代理
- 工程代理
- 设计代理
- 销售代理
- 产品代理
- 测试代理
- 财务代理
- 项目管理代理
- 付费媒体代理
- 专业代理
- 学术代理
- 游戏开发代理
- 空间计算代理

---

## 4. 核心数据模型

### 4.1 Task（任务模型）

**文件路径**: [app/models/models.py

```python
class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id: String (UUID)
    title: String (255)
    description: Text
    status: String (50) [pending, running, completed, failed, cancelled]
    priority: Integer
    input_data: JSON
    output_data: JSON
    error_message: Text
    created_at: DateTime
    updated_at: DateTime
    completed_at: DateTime
    user_id: String
    parent_task_id: String (ForeignKey)
```

**关系**：
- sub_tasks：一对多关系（子任务）
- executions：一对多关系（代理执行记录）

### 4.2 AgentExecution（代理执行记录）

```python
class AgentExecution(Base):
    """代理执行记录"""
    __tablename__ = "agent_executions"
    
    id: String (UUID)
    task_id: String (ForeignKey)
    agent_name: String (100)
    model_provider: String (50)
    model_name: String (100)
    status: String (50)
    input_tokens: Integer
    output_tokens: Integer
    cost: Float
    execution_time_ms: Integer
    started_at: DateTime
    completed_at: DateTime
    error_message: Text
    extra_data: JSON
```

### 4.3 Agent（代理配置）

```python
class Agent(Base):
    """代理配置"""
    __tablename__ = "agents"
    
    id: String (UUID)
    name: String (100, unique)
    description: Text
    category: String (50)
    source_file: String (255)
    model_provider: String (50)
    model_name: String (100)
    tools: JSON
    capabilities: JSON
    prompt_template: Text
    is_active: Boolean
    created_at: DateTime
    updated_at: DateTime
```

### 4.4 ModelProvider（模型提供者配置）

```python
class ModelProvider(Base):
    """模型提供者配置"""
    __tablename__ = "model_providers"
    
    id: String (UUID)
    name: String (50, unique)
    base_url: String (255)
    api_key_encrypted: Text
    models: JSON
    rate_limit: Integer
    is_active: Boolean
    created_at: DateTime
    updated_at: DateTime
```

### 4.5 Brain（大脑配置）

```python
class Brain(Base):
    """大脑配置"""
    __tablename__ = "brains"
    
    id: String (UUID)
    name: String (100, unique)
    brain_type: String (50)
    description: Text
    max_concurrent_tasks: Integer
    models: JSON
    agents: JSON
    capabilities: JSON
    is_active: Boolean
    created_at: DateTime
    updated_at: DateTime
```

---

## 5. 核心类与函数

### 5.1 代理相关类

#### 5.1.1 BaseAgent（代理基类）

**文件路径**: [app/agents/agent_base.py

**主要方法**：
| 方法 | 参数 | 返回类型 | 说明 |
|------|------|---------|------|
| execute | task: Dict[str, Any] | Dict[str, Any] | 执行任务（抽象方法） |
| get_prompt | task: Dict[str, Any] | str | 获取提示词（抽象方法） |
| validate_task | task: Dict[str, Any] | bool | 验证任务 |
| update_status | status: AgentStatus | None | 更新代理状态 |
| get_status | - | Dict[str, Any] | 获取代理状态 |

#### 5.1.2 AgentManager（代理管理器）

**主要方法**：
| 方法 | 参数 | 返回类型 | 说明 |
|------|------|---------|------|
| register_agent | agent_id: str, agent: BaseAgent | None | 注册代理 |
| get_agent | agent_id: str | Optional[BaseAgent] | 获取指定代理 |
| list_agents | - | List[Dict[str, Any]] | 列出所有代理 |
| get_agents_by_category | category: AgentCategory | List[BaseAgent] | 按类别获取代理 |
| execute_task | agent_id: str, task: Dict[str, Any] | Dict[str, Any] | 执行任务 |

### 5.2 大脑相关类

#### 5.2.1 Brain（大脑基类）

**文件路径**: [app/brains/brain_base.py

**主要方法**：
| 方法 | 参数 | 返回类型 | 说明 |
|------|------|---------|------|
| process_task | task: Dict[str, Any] | Dict[str, Any] | 处理任务（抽象方法） |
| select_agent | task: Dict[str, Any] | str | 选择子代理（抽象方法） |
| delegate_task | task: Dict[str, Any], agent_name: str | Dict[str, Any] | 委派任务给子代理 |
| collaborate | target_brain_id: str, task: Dict[str, Any] | None | 与其他大脑协作 |
| update_status | status: BrainStatus | None | 更新状态 |
| get_status | - | Dict[str, Any] | 获取状态 |

#### 5.2.2 BrainNetwork（大脑网络）

**主要方法**：
| 方法 | 参数 | 返回类型 | 说明 |
|------|------|---------|------|
| register_brain | brain_id: str, brain: Brain | None | 注册大脑 |
| connect_brains | brain1_id: str, brain2_id: str | None | 连接两个大脑 |
| send_message | message: BrainMessage | None | 发送消息 |
| receive_messages | brain_id: str | List[BrainMessage] | 接收消息 |
| broadcast | source_id: str, message_type: str, payload: Dict[str, Any] | None | 广播消息 |
| get_all_status | - | Dict[str, Any] | 获取所有大脑状态 |

#### 5.2.3 MasterBrain（主大脑）

**主要方法**：
| 方法 | 参数 | 返回类型 | 说明 |
|------|------|---------|------|
| register_sub_brain | brain_id: str, brain: Brain | None | 注册子大脑 |
| route_task | task: Dict[str, Any] | str | 路由任务到合适的大脑 |
| process_task | task: Dict[str, Any] | Dict[str, Any] | 处理任务 |
| select_agent | task: Dict[str, Any] | str | 选择子代理 |
| load_balance | - | Optional[str] | 负载均衡 - 找到负载最低的大脑 |
| get_all_status | - | Dict[str, Any] | 获取所有大脑状态 |

### 5.3 核心功能类

#### 5.3.1 Settings（应用配置）

**文件路径**: [app/core/config.py

**配置项**：
- APP_NAME: 应用名称
- APP_VERSION: 应用版本
- DEBUG: 调试模式
- HOST: 主机地址
- PORT: 端口号
- DATABASE_URL: 数据库连接
- QUEUE_TYPE: 队列类型
- CACHE_TYPE: 缓存类型
- MAX_AGENTS: 最大代理数
- MAX_CONCURRENT_TASKS: 最大并发任务数
- LOG_LEVEL: 日志级别
- LOG_FILE: 日志文件
- SECRET_KEY: 密钥
- ACCESS_TOKEN_EXPIRE_MINUTES: 访问令牌过期时间

#### 5.3.2 数据库相关函数

**文件路径**: [app/core/database.py

**函数**：
| 函数名 | 说明 |
|--------|------|
| get_db | 获取数据库会话 |
| init_db | 初始化数据库 |

### 5.4 API 路由

**文件路径**: [app/api/routes.py

#### 主要端点

| HTTP 方法 | 路径 | 说明 |
|-----------|------|------|
| GET | /health | 健康检查 |
| GET | /api/system/status | 系统状态 |
| POST | /api/tasks | 创建任务 |
| GET | /api/tasks | 获取任务列表 |
| GET | /api/tasks/{task_id} | 获取任务详情 |
| POST | /api/tasks/{task_id}/cancel | 取消任务 |
| POST | /api/agents | 创建代理 |
| GET | /api/agents | 获取代理列表 |
| GET | /api/agents/{agent_id} | 获取代理详情 |
| PUT | /api/agents/{agent_id} | 更新代理 |
| POST | /api/agents/{agent_id}/toggle | 启用/禁用代理 |
| POST | /api/brains | 创建大脑 |
| GET | /api/brains | 获取大脑列表 |
| GET | /api/brains/{brain_id} | 获取大脑详情 |
| PUT | /api/brains/{brain_id} | 更新大脑 |
| POST | /api/models | 创建模型 |
| GET | /api/models | 获取模型列表 |
| PUT | /api/models/{model_id} | 更新模型 |

---

## 6. 依赖关系与技术栈

### 6.1 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 开发语言 |
| FastAPI | 0.104.1 | Web框架 |
| Uvicorn | 0.24.0 | ASGI服务器 |
| SQLAlchemy | 2.0.23 | ORM框架 |
| Alembic | 1.13.0 | 数据库迁移 |
| Pydantic | 2.5.2 | 数据验证 |
| Pydantic Settings | 2.1.0 | 配置管理 |
| Loguru | 0.7.2 | 日志管理 |
| AioHTTP | 3.9.1 | 异步HTTP |
| AioSQLite | 0.19.0 | 异步SQLite |
| HTTPX | 0.25.2 | HTTP客户端 |
| Python Multipart | 0.0.6 | 表单解析 |
| Python JOSE | 3.3.0 | JWT处理 |
| Passlib | 1.7.4 | 密码哈希 |
| Psutil | 5.9.6 | 系统监控 |
| PyYAML | 6.0.1 | YAML解析 |

### 6.2 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.3.8 | 前端框架 |
| Vue Router | 4.2.5 | 路由管理 |
| Pinia | 2.1.7 | 状态管理 |
| Element Plus | 2.4.3 | UI组件库 |
| Axios | 1.6.2 | HTTP客户端 |
| Cytoscape | 3.27.0 | 可视化 |
| ECharts | 5.4.3 | 图表库 |
| Vite | 5.0.4 | 构建工具 |
| TypeScript | 5.3.2 | 类型系统 |

### 6.3 数据库

- SQLite (默认)
- PostgreSQL (可选)
- Redis (可选缓存)

---

## 7. 配置与部署

### 7.1 环境配置

**主要环境变量**（可在 .env 文件中配置）：

```env
APP_NAME=Agency AI System
APP_VERSION=0.1.0
DEBUG=False
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./data/agency.db
QUEUE_TYPE=memory
CACHE_TYPE=memory
MAX_AGENTS=2
MAX_CONCURRENT_TASKS=5
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 7.2 Docker 部署

**Docker Compose 配置**（文件路径**: [docker-compose.yml

服务说明：

| 服务 | 说明 | 端口映射 |
|------|------|--------|
| orchestrator | 总控服务 | 8000:8000 |
| agent-worker | 代理工作服务 | - |
| dashboard | 前端管理界面 | 3000:3000 |

**启动命令**：

```bash
# 使用 Docker Compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 7.3 本地开发

#### 后端启动

```bash
cd orchestrator
pip install -r requirements.txt
python main.py
```

#### 前端启动

```bash
cd dashboard
npm install
npm run dev
```

#### 访问地址

- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health
- 前端界面: http://localhost:3000

---

## 8. 代理和大脑配置

### 8.1 代理配置

**文件路径**: [app/config/agents_config.py

**代理类别**：

| 类别 | 说明 | 代理数量 |
|------|------|---------|
| marketing | 营销策略、内容创作、社交媒体 | 4 |
| engineering | 软件开发、架构设计、代码审查 | 6 |
| design | UI/UX设计、视觉设计、品牌设计 | 3 |
| sales | 销售策略、客户管理、管道分析 | 3 |
| product | 产品管理、用户研究、反馈分析 | 2 |
| testing | 测试自动化、性能测试、质量保证 | 2 |
| finance | 财务分析、预算管理、税务策略 | 2 |
| project-management | 项目规划、执行监控、风险管理 | 1 |
| paid-media | PPC策略、付费社交、广告优化 | 2 |
| specialized | 法律、招聘、翻译等专业领域 | 3 |
| academic | 历史研究、心理学分析等学术领域 | 2 |
| game-development | 游戏设计、关卡设计、叙事设计 | 1 |
| spatial-computing | XR开发、空间计算、沉浸式体验 | 1 |

### 8.2 大脑配置

每个大脑都包含相应的代理配置，包括：

- 名称
- 类型
- 描述
- 最大并发任务数
- 可用模型
- 代理列表
- 能力列表

---

## 9. 服务层

### 9.1 心跳服务

**功能**：
- 监控系统组件健康状态
- 定期发送心跳信号
- 记录组件状态变更

### 9.2 审计服务

**功能**：
- 记录系统事件
- 任务创建/取消日志
- 代理创建/更新/切换日志
- 大脑创建/更新日志
- 系统启动/关闭日志

### 9.3 进度监控服务

**功能**：
- 监控任务执行进度
- 实时更新任务状态
- 记录执行记录

---

## 10. 开发指南

### 10.1 添加新代理

1. 在 `app/agents/` 目录下创建新代理类，继承自 `BaseAgent`
2. 实现 `execute` 和 `get_prompt` 抽象方法
3. 在 `app/config/agents_config.py` 中添加代理配置
4. 在 `app/agents/manager.py` 中注册代理

### 10.2 添加新大脑

1. 在 `app/brains/` 目录下创建新大脑类，继承自 `Brain`
2. 实现 `process_task` 和 `select_agent` 抽象方法
3. 在 `app/config/agents_config.py` 中添加大脑配置
4. 在 `app/brains/manager.py` 中注册大脑

### 10.3 添加新 API 端点

1. 在 `app/api/` 目录下创建或修改路由文件
2. 在 `app/api/routes.py` 中注册路由
3. 使用 Pydantic 模型定义请求/响应格式

---

## 11. 测试

### 11.1 运行测试

```bash
cd orchestrator
python -m pytest tests/ -v
```

### 11.2 测试覆盖

- 代理测试
- API测试
- 大脑测试
- 数据库测试
- 集成测试

---

## 12. 变更日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

---

## 13. 许可证

MIT License

---

## 14. 联系

更多信息参考文档目录中的 [README.md](README.md)
