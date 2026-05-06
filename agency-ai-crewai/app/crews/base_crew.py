"""Crew基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from crewai import Crew, Process, Agent, Task
from app.agents.base_agent import BaseAgentFactory
from app.tasks.base_task import BaseTaskFactory
from loguru import logger


class BaseCrew(ABC):
    """Crew基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.agents: Dict[str, Agent] = {}
        self.agent_factory: Optional[BaseAgentFactory] = None
        self.task_factory: Optional[BaseTaskFactory] = None
        self.completed_tasks = 0
        self.failed_tasks = 0
    
    def initialize(self):
        """初始化Crew"""
        if self.agent_factory:
            self.agents = self.agent_factory.create_agents()
            logger.info(f"{self.name} 初始化完成，共 {len(self.agents)} 个代理")
    
    async def execute(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务"""
        logger.info(f"{self.name} 开始执行任务")
        
        # 创建任务
        tasks = self.task_factory.create_tasks(self.agents, task_config)
        
        if not tasks:
            return {"status": "error", "message": "没有可用的任务"}
        
        # 创建Crew
        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # 执行
        try:
            result = crew.kickoff()
            self.completed_tasks += 1
            logger.info(f"{self.name} 任务完成")
            return {
                "status": "completed",
                "output": result,
                "crew": self.name,
                "completed_tasks": self.completed_tasks
            }
        except Exception as e:
            self.failed_tasks += 1
            logger.error(f"{self.name} 任务失败: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "crew": self.name,
                "failed_tasks": self.failed_tasks
            }
    
    def get_agent_count(self) -> int:
        """获取代理数量"""
        return len(self.agents)
    
    def get_completed_tasks(self) -> int:
        """获取完成任务数"""
        return self.completed_tasks
    
    def get_failed_tasks(self) -> int:
        """获取失败任务数"""
        return self.failed_tasks
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "name": self.name,
            "description": self.description,
            "agents": len(self.agents),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "status": "ready"
        }
