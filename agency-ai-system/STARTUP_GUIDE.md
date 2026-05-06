# Agency AI System - 启动指南

## 📋 前提条件

在启动项目之前，请确保已安装以下软件：

### 必需软件

1. **Python 3.10 或更高版本**
   - 下载地址：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **Node.js 18 或更高版本**
   - 下载地址：https://nodejs.org/
   - 推荐安装 LTS 版本

3. **Docker Desktop (可选，推荐用于生产环境)**
   - 下载地址：https://www.docker.com/products/docker-desktop/

### 验证安装

打开终端并运行以下命令验证：

```bash
# 检查 Python 版本
python --version
# 应显示 Python 3.10.x 或更高版本

# 检查 Node.js 版本
node --version
# 应显示 v18.x.x 或更高版本

# 检查 npm 版本
npm --version
# 应显示 8.x.x 或更高版本
```

---

## 🚀 启动方式

### 方式一：使用 Docker Compose (推荐)

这是最简单的方式，适合生产环境。

```bash
# 1. 进入项目目录
cd agency-ai-system

# 2. 复制环境变量文件
copy .env.example .env

# 3. 启动所有服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 停止服务
docker-compose down
```

**访问地址：**
- 🌐 前端界面：http://localhost:3000
- 📚 API 文档：http://localhost:8000/docs
- 💚 健康检查：http://localhost:8000/health

---

### 方式二：本地开发模式

适合开发和调试。

#### 第一步：准备后端

```bash
# 1. 进入项目目录
cd agency-ai-system

# 2. 进入后端目录
cd orchestrator

# 3. 创建虚拟环境（推荐）
python -m venv venv

# 4. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 创建必要目录
mkdir -p data
mkdir -p logs
```

#### 第二步：启动后端服务

```bash
# 在 orchestrator 目录下
python main.py
```

您应该会看到类似输出：

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### 第三步：准备前端

打开一个新的终端窗口：

```bash
# 1. 进入前端目录
cd agency-ai-system/dashboard

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

您应该会看到类似输出：

```
  VITE v5.0.4  ready in 123 ms

  ➜  Local:   http://localhost:3000/
```

---

## ✅ 验证安装

启动服务后，请访问以下地址验证系统是否正常运行：

### 1. 健康检查
访问：http://localhost:8000/health

应该返回：
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### 2. API 文档
访问：http://localhost:8000/docs

这是 FastAPI 的交互式 API 文档，您可以在这里测试所有 API 端点。

### 3. 前端界面
访问：http://localhost:3000

您应该能看到 Agency AI System 的管理界面。

---

## 🔧 常见问题

### 问题 1：端口已被占用

如果端口 8000 或 3000 被占用，您可以：

**修改后端端口：**
编辑 `orchestrator/app/core/config.py`，修改 `PORT` 值。

**修改前端端口：**
编辑 `dashboard/vite.config.ts`，修改服务器端口。

**或停止占用端口的程序：**
```bash
# Windows 查找占用端口的进程
netstat -ano | findstr :8000

# 停止进程
taskkill /PID <进程ID> /F
```

### 问题 2：依赖安装失败

**Python 依赖：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装单个依赖
pip install <包名>
```

**Node.js 依赖：**
```bash
# 清理缓存
npm cache clean --force

# 重新安装
rm -rf node_modules
npm install
```

### 问题 3：数据库初始化错误

如果遇到数据库错误：

```bash
# 删除旧的数据库文件
cd orchestrator
del data\agency.db

# 重新启动应用
python main.py
```

### 问题 4：找不到 Python 或 Node.js

确保它们已添加到系统 PATH：

**Windows：**
1. 右键点击"此电脑" → 属性 → 高级系统设置
2. 点击"环境变量"
3. 在"系统变量"中找到"Path"，双击编辑
4. 添加 Python 和 Node.js 的安装路径
5. 点击确定并重启终端

**Linux/Mac：**
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export PATH="/usr/local/bin:/usr/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
```

---

## 📊 启动后可以做什么

### 1. 创建任务
通过 API 或前端界面创建新任务

### 2. 查看代理状态
查看所有注册的代理及其状态

### 3. 查看大脑状态
查看所有大脑的工作状态

### 4. 监控进度
实时监控任务执行进度

### 5. 查看审计日志
查看系统操作日志

---

## 🛠️ 开发模式提示

### 启用调试模式

编辑 `.env` 文件：

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### 添加新的代理

1. 在 `orchestrator/app/agents/` 目录下创建新的代理文件
2. 继承 `BaseAgent` 类
3. 实现 `execute()` 和 `get_prompt()` 方法
4. 在 `manager.py` 中注册新代理

### 添加新的大脑

1. 在 `orchestrator/app/brains/` 目录下创建新的大脑文件
2. 继承 `Brain` 类
3. 实现 `process_task()` 和 `select_agent()` 方法
4. 在 `manager.py` 中注册新大脑

---

## 📞 获取帮助

如果遇到问题：

1. 查看项目文档：
   - [README.md](README.md) - 项目说明
   - [CODE_WIKI.md](CODE_WIKI.md) - 代码知识库
   - [PROJECT_INSPECTION_REPORT.md](PROJECT_INSPECTION_REPORT.md) - 项目检测报告

2. 查看日志文件：
   - 后端日志：`orchestrator/logs/app.log`
   - Docker 日志：`docker-compose logs -f`

3. 查看 API 文档：
   - FastAPI 自动生成的文档：http://localhost:8000/docs

---

## 🎉 成功启动！

如果一切正常，您应该能够：

- ✅ 访问前端界面
- ✅ 访问 API 文档
- ✅ 创建和管理任务
- ✅ 查看代理和大脑状态
- ✅ 监控系统运行状态

恭喜！Agency AI System 已成功启动！ 🚀

---

**最后更新：** 2026-05-05
**项目版本：** 0.1.0
