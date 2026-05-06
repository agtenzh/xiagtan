"""数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")  # pending, running, completed, failed, cancelled
    priority = Column(Integer, default=0)
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    user_id = Column(String)
    parent_task_id = Column(String, ForeignKey("tasks.id"))
    
    # 关系
    sub_tasks = relationship("Task", backref="parent_task", remote_side=[id])
    executions = relationship("AgentExecution", back_populates="task")


class AgentExecution(Base):
    """代理执行记录"""
    __tablename__ = "agent_executions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"))
    agent_name = Column(String(100), nullable=False)
    model_provider = Column(String(50))
    model_name = Column(String(100))
    status = Column(String(50), default="pending")
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    cost = Column(Float)
    execution_time_ms = Column(Integer)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    extra_data = Column(JSON)  # 原名 metadata，改为 extra_data 避免保留名冲突
    
    # 关系
    task = relationship("Task", back_populates="executions")


class Agent(Base):
    """代理配置"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50))
    source_file = Column(String(255))
    model_provider = Column(String(50))
    model_name = Column(String(100))
    tools = Column(JSON)
    capabilities = Column(JSON)
    prompt_template = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelProvider(Base):
    """模型提供者配置"""
    __tablename__ = "model_providers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    base_url = Column(String(255))
    api_key_encrypted = Column(Text)
    models = Column(JSON)
    rate_limit = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Brain(Base):
    """大脑配置"""
    __tablename__ = "brains"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    brain_type = Column(String(50))  # master, marketing, development, design, sales, analytics
    description = Column(Text)
    max_concurrent_tasks = Column(Integer, default=5)
    models = Column(JSON)
    agents = Column(JSON)
    capabilities = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
