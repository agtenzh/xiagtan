"""数据模型"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, Float
from datetime import datetime
import uuid

from app.core.database import Base


def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())


class Brain(Base):
    """大脑模型"""
    __tablename__ = "brains"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    brain_type = Column(String(50), nullable=False)  # master, marketing, engineering, etc.
    description = Column(Text)
    max_concurrent_tasks = Column(Integer, default=5)
    models = Column(JSON)  # 可用模型列表
    agents = Column(JSON)  # 代理列表
    capabilities = Column(JSON)  # 能力列表
    is_active = Column(Boolean, default=True)
    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Agent(Base):
    """代理模型"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    role = Column(String(200))
    goal = Column(Text)
    backstory = Column(Text)
    category = Column(String(50))  # marketing, engineering, design, etc.
    model_provider = Column(String(50))
    model_name = Column(String(100))
    tools = Column(JSON)
    capabilities = Column(JSON)
    is_active = Column(Boolean, default=True)
    tasks_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=0)
    brain_id = Column(String)  # 分配的大脑
    agent_id = Column(String)  # 分配的代理
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)


class ModelProvider(Base):
    """模型提供者"""
    __tablename__ = "model_providers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    provider_type = Column(String(50))  # openai, anthropic, local
    base_url = Column(String(255))
    api_key_encrypted = Column(Text)
    models = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """审计日志"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(String(20), default="INFO")
    category = Column(String(50), index=True)
    action = Column(String(100), index=True)
    target_type = Column(String(50))
    target_id = Column(String(100))
    target_name = Column(String(200))
    actor = Column(String(100))
    details = Column(JSON)
    message = Column(Text)
