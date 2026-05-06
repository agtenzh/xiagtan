"""营销大脑"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.brains.brain_base import Brain, BrainConfig, BrainType
from app.config.agents_config import MARKETING_BRAIN_CONFIG


class MarketingBrain(Brain):
    """营销大脑"""
    
    def __init__(self):
        config = BrainConfig(
            name=MARKETING_BRAIN_CONFIG["name"],
            brain_type=BrainType.MARKETING,
            description=MARKETING_BRAIN_CONFIG["description"],
            max_concurrent_tasks=MARKETING_BRAIN_CONFIG["max_concurrent_tasks"],
            models=MARKETING_BRAIN_CONFIG["models"],
            agents=MARKETING_BRAIN_CONFIG["agents"],
            capabilities=MARKETING_BRAIN_CONFIG["capabilities"]
        )
        super().__init__(config)
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理营销相关任务"""
        logger.info(f"营销大脑处理任务: {task.get('title', '未知')}")
        return {
            "status": "processed",
            "brain": self.config.name,
            "task_id": task.get("id")
        }
    
    def select_agent(self, task: Dict[str, Any]) -> str:
        """根据任务选择合适的代理"""
        task_type = task.get("type", "content")
        
        if task_type == "content":
            return "content_creator"
        elif task_type == "seo":
            return "seo_expert"
        elif task_type == "social":
            return "social_media"
        else:
            return "content_creator"
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """执行营销任务"""
        logger.info(f"营销大脑执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        
        return {
            "status": "completed",
            "brain": self.config.name,
            "output": f"营销任务完成: {task.get('title', '未知')}",
            "agent_used": self.select_agent(task)
        }
