AI多代理系统 (CrewAI版本)
基于 CrewAI 框架的 AI 多代理系统。

特性
🧠 多Crew架构：支持多个专业Crew协作
🤖 CrewAI代理：基于CrewAI的标准化代理
🎨 可视化界面：Vue.js管理界面
📊 实时监控：系统状态和任务监控
⚙️ 自适应配置：根据服务器配置自动调整
快速开始
安装依赖
pip install -r requirements.txt
配置环境
cp .env.example .env
# 编辑 .env 文件，配置 API 密钥
启动服务
python main.py
访问
API文档: http://localhost:8000/docs
健康检查: http://localhost:8000/health
项目结构
agency-ai-crewai/
├── app/
│   ├── crews/        # Crew定义
│   ├── agents/       # Agent定义
│   ├── tasks/        # Task定义
│   ├── tools/        # 工具
│   ├── api/          # API接口
│   ├── core/         # 核心配置
│   ├── models/       # 数据模型
│   └── services/     # 业务服务
├── dashboard/        # Vue.js前端
├── config/           # 配置文件
├── tests/            # 测试
├── docs/             # 文档
├── main.py           # 主入口
└── requirements.txt  # 依赖
API接口
方法	路径	说明
GET	/health	健康检查
GET	/api/system/status	系统状态
GET	/api/brains	获取所有大脑
POST	/api/brains	创建大脑
GET	/api/brains/{id}	获取大脑详情
GET	/api/brains/{id}/status	获取大脑状态
POST	/api/brains/{id}/execute	执行任务
GET	/api/agents	获取所有代理
GET	/api/tasks	获取任务列表
POST	/api/tasks	创建任务
技术栈
后端: Python 3.10+ / FastAPI / CrewAI
前端: Vue.js 3 / TypeScript / Element Plus
数据库: SQLite / PostgreSQL
AI: OpenAI GPT-4 / LangChain
