# AI多代理系统 - API文档

## 概述

AI多代理系统的RESTful API文档。

基础URL: `http://localhost:8000`

## 认证

当前版本不需要认证。

## API列表

### 健康检查

#### GET /health
系统健康检查

**响应示例:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### 系统状态

#### GET /api/system/status
获取系统状态

**响应示例:**
```json
{
  "cpu_usage": 25.5,
  "memory_usage": 45.2,
  "disk_usage": 60.0,
  "active_tasks": 3,
  "active_agents": 5,
  "active_brains": 6,
  "uptime": 3600
}
```

### 任务管理

#### POST /api/tasks
创建任务

**请求体:**
```json
{
  "title": "任务标题",
  "description": "任务描述",
  "priority": 5,
  "input_data": {}
}
```

#### GET /api/tasks
获取任务列表

**查询参数:**
- `status`: 任务状态过滤 (pending, running, completed, failed, cancelled)

#### GET /api/tasks/{task_id}
获取任务详情

#### POST /api/tasks/{task_id}/cancel
取消任务

### 代理管理

#### POST /api/agents
创建代理

#### GET /api/agents
获取代理列表

#### GET /api/agents/{agent_id}
获取代理详情

#### PUT /api/agents/{agent_id}
更新代理

#### POST /api/agents/{agent_id}/toggle
启用/禁用代理

### 大脑管理

#### POST /api/brains
创建大脑

#### GET /api/brains
获取大脑列表

#### GET /api/brains/{brain_id}
获取大脑详情

#### PUT /api/brains/{brain_id}
更新大脑

### 模型管理

#### POST /api/models
创建模型

#### GET /api/models
获取模型列表

#### PUT /api/models/{model_id}
更新模型

### 审计日志

#### GET /api/logs
查询日志

**查询参数:**
- `category`: 日志类别 (task, agent, brain, system)
- `action`: 操作类型 (create, update, delete, execute, complete, fail)
- `level`: 日志级别 (INFO, SUCCESS, WARNING, ERROR)
- `hours`: 查询最近N小时的日志
- `limit`: 返回数量 (默认100)
- `offset`: 偏移量

#### GET /api/logs/recent
获取最近日志

#### GET /api/logs/category/{category}
按类别获取日志

#### GET /api/logs/errors
获取错误日志

#### GET /api/logs/success
获取成功日志

#### GET /api/logs/task/{task_id}
获取任务历史

#### GET /api/logs/agent/{agent_id}
获取代理历史

#### GET /api/logs/statistics
获取日志统计

#### GET /api/logs/search?keyword=xxx
搜索日志

#### GET /api/logs/timeline
获取时间线

#### GET /api/logs/summary
获取日志摘要

### 心跳检测

#### GET /api/heartbeat/status
获取所有组件心跳状态

#### GET /api/heartbeat/component/{component_id}
获取指定组件心跳状态

#### POST /api/heartbeat/beat/{component_id}
发送心跳

#### POST /api/heartbeat/error/{component_id}
发送错误心跳

#### POST /api/heartbeat/register
注册组件

#### DELETE /api/heartbeat/unregister/{component_id}
注销组件

#### GET /api/heartbeat/unhealthy
获取不健康的组件

#### GET /api/heartbeat/health
系统健康检查

### 进度监控

#### GET /api/progress/status
获取所有进度状态

#### GET /api/progress/task/{task_id}
获取任务进度

#### GET /api/progress/report
获取进度报告

#### POST /api/progress/task/{task_id}/progress
更新任务进度

#### POST /api/progress/task/{task_id}/complete
完成任务

#### POST /api/progress/task/{task_id}/fail
任务失败

#### POST /api/progress/thread/{thread_id}/status
更新线程状态

#### GET /api/progress/threads
获取所有线程状态
