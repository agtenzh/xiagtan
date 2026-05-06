# 访问指南

## 服务地址

| 服务 | 地址 | 状态 |
|------|------|------|
| **前端界面** | http://localhost:3000 | ✅ 运行中 |
| **后端API** | http://localhost:8000 | ✅ 运行中 |
| **API文档** | http://localhost:8000/docs | ✅ 可访问 |

## 如果无法访问

### 方法1：清除浏览器缓存
1. 按 `Ctrl + Shift + Delete`
2. 选择"缓存的图片和文件"
3. 点击"清除数据"
4. 重新访问 http://localhost:3000

### 方法2：使用无痕模式
1. 按 `Ctrl + Shift + N` 打开无痕窗口
2. 访问 http://localhost:3000

### 方法3：强制刷新
1. 在浏览器中按 `Ctrl + F5` 强制刷新页面

### 方法4：检查服务状态
```bash
# 检查端口是否在监听
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"

# 测试后端API
curl http://localhost:8000/health

# 测试前端
curl http://localhost:3000
```

## 可访问的页面

| 页面 | 地址 | 说明 |
|------|------|------|
| 首页 | http://localhost:3000/ | 系统概览 |
| 系统监控 | http://localhost:3000/dashboard | 实时监控 |
| 代理管理 | http://localhost:3000/agents | 管理代理 |
| 模型配置 | http://localhost:3000/models | 配置模型 |
| 任务管理 | http://localhost:3000/tasks | 管理任务 |
| 日志查看 | http://localhost:3000/logs | 查看日志 |
| 配置管理 | http://localhost:3000/config | 系统配置 |
| 系统设置 | http://localhost:3000/settings | 高级设置 |

## 启动服务

如果服务未运行，请按以下步骤启动：

### 启动后端
```bash
cd orchestrator
pip install -r requirements.txt
python main.py
```

### 启动前端
```bash
cd dashboard
npm install
npm run dev
```
