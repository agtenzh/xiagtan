"""代理基类"""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from loguru import logger


class AgentStatus(str, Enum):
    """代理状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentCategory(str, Enum):
    """代理类别"""
    MARKETING = "marketing"
    DESIGN = "design"
    PAID_MEDIA = "paid_media"
    SALES = "sales"
    DEVELOPMENT = "development"
    PRODUCT = "product"
    TESTING = "testing"
    FINANCE = "finance"
    PROJECT_MANAGEMENT = "project_management"
    SPECIALIZED = "specialized"
    ACADEMIC = "academic"
    GAME_DEVELOPMENT = "game_development"
    SPATIAL_COMPUTING = "spatial_computing"


@dataclass
class AgentConfig:
    """代理配置"""
    name: str
    description: str
    category: AgentCategory
    model_provider: str = "openai"
    model_name: str = "gpt-3.5-turbo"
    tools: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    prompt_template: str = ""
    max_concurrent: int = 1
    timeout: int = 120


class BaseAgent(ABC):
    """代理基类"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self.current_tasks: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.last_used = datetime.now()
        logger.info(f"代理 {self.config.name} 初始化完成")
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务"""
        pass
    
    @abstractmethod
    def get_prompt(self, task: Dict[str, Any]) -> str:
        """获取提示词"""
        pass
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """验证任务"""
        return True
    
    def update_status(self, status: AgentStatus):
        """更新状态"""
        self.status = status
        self.last_used = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "name": self.config.name,
            "description": self.config.description,
            "category": self.config.category.value,
            "status": self.status.value,
            "model": f"{self.config.model_provider}/{self.config.model_name}",
            "tools": self.config.tools,
            "capabilities": self.config.capabilities,
            "current_tasks": len(self.current_tasks),
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat()
        }


class AgentManager:
    """代理管理器"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        logger.info("代理管理器初始化完成")
    
    def register_agent(self, agent_id: str, agent: BaseAgent):
        """注册代理"""
        self.agents[agent_id] = agent
        logger.info(f"代理 {agent_id} ({agent.config.name}) 已注册")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """获取代理"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有代理"""
        return [
            {"id": agent_id, **agent.get_status()}
            for agent_id, agent in self.agents.items()
        ]
    
    def get_agents_by_category(self, category: AgentCategory) -> List[BaseAgent]:
        """按类别获取代理"""
        return [
            agent for agent in self.agents.values()
            if agent.config.category == category
        ]
    
    async def execute_task(self, agent_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"代理 {agent_id} 不存在")
        
        if agent.status != AgentStatus.IDLE:
            raise ValueError(f"代理 {agent_id} 正在忙碌")
        
        agent.update_status(AgentStatus.BUSY)
        try:
            result = await agent.execute(task)
            agent.update_status(AgentStatus.IDLE)
            return result
        except Exception as e:
            agent.update_status(AgentStatus.ERROR)
            raise


# 全局代理管理器
agent_manager = AgentManager()
