"""数据模型Schema"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


class BrainType(str, Enum):
    MASTER = "master"
    MARKETING = "marketing"
    DEVELOPMENT = "development"
    DESIGN = "design"
    SALES = "sales"
    ANALYTICS = "analytics"


# 任务Schema
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 0
    input_data: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: int
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# 代理Schema
class AgentCreate(BaseModel):
    model_config = {'protected_namespaces': ()}
    
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    tools: Optional[List[str]] = None
    capabilities: Optional[List[str]] = None
    prompt_template: Optional[str] = None


class AgentResponse(BaseModel):
    model_config = {'protected_namespaces': (), 'from_attributes': True}
    
    id: str
    name: str
    description: Optional[str]
    category: Optional[str]
    model_provider: Optional[str]
    model_name: Optional[str]
    tools: Optional[List[str]]
    capabilities: Optional[List[str]]
    prompt_template: Optional[str] = None
    is_active: bool
    created_at: datetime


# 大脑Schema
class BrainCreate(BaseModel):
    name: str
    brain_type: str
    description: Optional[str] = None
    max_concurrent_tasks: int = 5
    models: Optional[List[str]] = None
    agents: Optional[List[str]] = None
    capabilities: Optional[List[str]] = None


class BrainResponse(BaseModel):
    model_config = {'from_attributes': True}
    
    id: str
    name: str
    brain_type: str
    description: Optional[str]
    max_concurrent_tasks: int
    models: Optional[List[str]]
    agents: Optional[List[str]]
    capabilities: Optional[List[str]]
    is_active: bool
    created_at: datetime


# 模型Schema
class ModelProviderCreate(BaseModel):
    name: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    models: Optional[List[Dict[str, Any]]] = None
    rate_limit: Optional[int] = None


class ModelProviderResponse(BaseModel):
    id: str
    name: str
    base_url: Optional[str]
    models: Optional[List[Dict[str, Any]]]
    rate_limit: Optional[int]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 系统状态Schema
class SystemStatus(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_tasks: int
    active_agents: int
    active_brains: int
    uptime: float


# 代理执行Schema
class AgentExecutionResponse(BaseModel):
    model_config = {'protected_namespaces': (), 'from_attributes': True}
    
    id: str
    task_id: str
    agent_name: str
    model_provider: Optional[str]
    model_name: Optional[str]
    status: str
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    cost: Optional[float]
    execution_time_ms: Optional[int]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
