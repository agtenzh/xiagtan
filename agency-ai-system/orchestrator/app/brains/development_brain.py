"""开发大脑"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.brains.brain_base import Brain, BrainConfig, BrainType
from app.config.agents_config import DEVELOPMENT_BRAIN_CONFIG


class DevelopmentBrain(Brain):
    """开发大脑"""
    
    def __init__(self):
        config = BrainConfig(
            name=DEVELOPMENT_BRAIN_CONFIG["name"],
            brain_type=BrainType.DEVELOPMENT,
            description=DEVELOPMENT_BRAIN_CONFIG["description"],
            max_concurrent_tasks=DEVELOPMENT_BRAIN_CONFIG["max_concurrent_tasks"],
            models=DEVELOPMENT_BRAIN_CONFIG["models"],
            agents=DEVELOPMENT_BRAIN_CONFIG["agents"],
            capabilities=DEVELOPMENT_BRAIN_CONFIG["capabilities"]
        )
        super().__init__(config)
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理开发相关任务"""
        logger.info(f"开发大脑处理任务: {task.get('title', '未知')}")
        return {
            "status": "processed",
            "brain": self.config.name,
            "task_id": task.get("id")
        }
    
    def select_agent(self, task: Dict[str, Any]) -> str:
        """根据任务选择合适的代理"""
        task_type = task.get("type", "code")
        
        if task_type == "code":
            return "code_generator"
        elif task_type == "test":
            return "test_writer"
        elif task_type == "deploy":
            return "deployer"
        else:
            return "code_generator"
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行开发任务"""
        logger.info(f"开发大脑执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        
        return {
            "status": "completed",
            "brain": self.config.name,
            "output": f"开发任务完成: {task.get('title', '未知')}",
            "agent_used": self.select_agent(task)
        }
