# AI多代理系统 (Agency AI System)

一个稳定、可自定义的AI多代理系统，支持多个专业大脑协作、40+个子代理执行任务、可视化思维导图界面。

## 特性

- **多大脑架构**：支持多个专业大脑协作处理复杂任务
- **40+子代理**：营销、开发、设计、销售、分析等领域代理
- **可视化界面**：思维导图展示大脑和代理关系
- **自适应配置**：根据服务器配置自动调整系统参数
- **实时监控**：CPU、内存、任务、代理状态监控

## 快速开始

```bash
# 安装后端依赖
cd orchestrator
pip install -r requirements.txt

# 安装前端依赖
cd ../dashboard
npm install

# 启动后端
cd ../orchestrator
python main.py

# 启动前端
cd ../dashboard
npm run dev
```

## 技术栈

- **后端**：Python 3.10+ / FastAPI / asyncio
- **前端**：Vue.js 3 / TypeScript / Vite
- **数据库**：PostgreSQL / SQLite / Redis
- **容器化**：Docker / Docker Compose

## 文档

- [架构规划文档](architecture_plan.md)
- [AI执行指令文档](ai_execution_plan.md)
- [变更日志](CHANGELOG.md)
