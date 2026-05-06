"""Pydantic模型"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BrainType(str, Enum):
    MASTER = "master"
    MARKETING = "marketing"
    ENGINEERING = "engineering"
    DESIGN = "design"
    SALES = "sales"
    ANALYTICS = "analytics"


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
    id: str
    name: str
    brain_type: str
    description: Optional[str]
    max_concurrent_tasks: int
    models: Optional[List[str]]
    agents: Optional[List[str]]
    capabilities: Optional[List[str]]
    is_active: bool
    tasks_completed: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class BrainStatus(BaseModel):
    brain_id: str
    name: str
    status: str
    agents: int
    tasks_completed: int
    tasks_pending: int


# 代理Schema
class AgentCreate(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str
    category: str
    model_provider: str = "openai"
    model_name: str = "gpt-4"
    tools: Optional[List[str]] = None
    capabilities: Optional[List[str]] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    goal: str
    backstory: str
    category: str
    model_provider: str
    model_name: str
    tools: Optional[List[str]]
    capabilities: Optional[List[str]]
    is_active: bool
    tasks_completed: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# 任务Schema
class TaskCreate(BaseModel):
    title: str
    description: str
    brain_id: Optional[str] = None
    agent_id: Optional[str] = None
    priority: int = 0
    input_data: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: int
    brain_id: Optional[str]
    agent_id: Optional[str]
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    execution_time_ms: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# 模型Schema
class ModelProviderCreate(BaseModel):
    name: str
    provider_type: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    models: Optional[List[Dict[str, Any]]] = None


class ModelProviderResponse(BaseModel):
    id: str
    name: str
    provider_type: str
    base_url: Optional[str]
    models: Optional[List[Dict[str, Any]]]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 系统状态Schema
class SystemStatus(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_brains: int
    active_agents: int
    running_tasks: int
    completed_tasks: int
    uptime: float
