"""审计日志模型"""
from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime
import uuid

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(String(20), default="INFO")  # INFO, WARNING, ERROR, SUCCESS
    category = Column(String(50), index=True)  # task, agent, brain, system, user
    action = Column(String(100), index=True)  # create, update, delete, execute, complete, fail
    target_type = Column(String(50))  # task, agent, brain, model
    target_id = Column(String(100))
    target_name = Column(String(200))
    actor = Column(String(100))  # user, system, brain_name, agent_name
    details = Column(JSON)
    message = Column(Text)
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "level": self.level,
            "category": self.category,
            "action": self.action,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "actor": self.actor,
            "details": self.details,
            "message": self.message
        }
