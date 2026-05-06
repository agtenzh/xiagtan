# AI多代理系统 - 用户手册

## 概述

AI多代理系统是一个稳定、可自定义的AI多代理系统，支持多个专业大脑协作、40+个子代理执行任务、可视化思维导图界面。

## 快速开始

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd agency-ai-system

# 安装后端依赖
cd orchestrator
pip install -r requirements.txt

# 安装前端依赖
cd ../dashboard
npm install
```

### 启动

```bash
# 启动后端
cd orchestrator
python main.py

# 启动前端
cd ../dashboard
npm run dev
```

### 访问

- 前端界面: http://localhost:3000
- API文档: http://localhost:8000/docs

## 功能说明

### 1. 首页

首页显示系统概览，包括：
- CPU使用率
- 内存使用率
- 活跃任务数
- 活跃代理数
- 快速操作按钮

### 2. 系统监控

系统监控页面显示：
- 系统健康状态
- 任务统计
- 运行中的任务
- 实时刷新（每10秒）

### 3. 代理管理

代理管理页面可以：
- 查看所有代理列表
- 添加新代理
- 编辑代理配置
- 启用/禁用代理

### 4. 模型配置

模型配置页面可以：
- 查看所有模型
- 添加新模型
- 配置API端点和密钥
- 测试模型连接

### 5. 任务管理

任务管理页面可以：
- 查看任务列表
- 创建新任务
- 取消任务
- 按状态筛选任务

### 6. 日志查看

日志查看页面可以：
- 查看所有日志
- 按类别筛选
- 按级别筛选
- 搜索日志

### 7. 配置管理

配置管理页面可以：
- 管理系统配置
- 管理模型配置
- 管理代理配置
- 管理大脑配置

### 8. 思维导图

思维导图页面可以：
- 可视化大脑和代理关系
- 拖拽节点
- 缩放视图
- 查看节点详情

## 配置说明

### 系统配置

系统配置文件位于 `config/` 目录：
- `low_config.yaml`: 低配置模式（2核2GB）
- `medium_config.yaml`: 中配置模式（4核4GB）
- `high_config.yaml`: 高配置模式（8核8GB+）
- `ultra_config.yaml`: 超高配置模式（16核16GB+）

### 环境变量

创建 `.env` 文件配置环境变量：

```env
# 数据库
DATABASE_URL=sqlite:///./data/agency.db

# 模型API
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# 日志
LOG_LEVEL=INFO
```

## 常见问题

### Q: 如何添加新的代理？

A: 在代理管理页面点击"添加代理"按钮，填写代理信息即可。

### Q: 如何切换配置模式？

A: 系统会自动检测服务器配置并选择最优模式。也可以在配置管理页面手动切换。

### Q: 如何查看任务执行日志？

A: 在日志查看页面，按类别"task"筛选即可查看所有任务相关日志。

### Q: 如何监控系统健康状态？

A: 在系统监控页面可以实时查看系统健康状态，包括CPU、内存、任务、代理等信息。
