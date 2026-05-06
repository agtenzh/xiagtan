"""设计代理"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory


class UIUXDesignerAgent(BaseAgent):
    """UI/UX设计师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="UI/UX设计师",
            description="User interface and experience design specialist",
            category=AgentCategory.DESIGN,
            model_provider="openai",
            model_name="gpt-4",
            tools=["design_system", "wireframing"],
            capabilities=["ui_design", "ux_research", "prototyping"],
            prompt_template="你是一个专业的UI/UX设计师。请根据以下任务进行设计：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"UI/UX设计师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"UI/UX设计完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class GraphicDesignerAgent(BaseAgent):
    """平面设计师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="平面设计师",
            description="Visual design and branding specialist",
            category=AgentCategory.DESIGN,
            model_provider="openai",
            model_name="gpt-4",
            tools=["image_generation", "color_palette"],
            capabilities=["branding", "print_design", "digital_assets"],
            prompt_template="你是一个专业的平面设计师。请根据以下任务进行设计：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"平面设计师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"平面设计完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class BrandingAgent(BaseAgent):
    """品牌设计代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="品牌设计师",
            description="Brand identity and style guide development specialist",
            category=AgentCategory.DESIGN,
            model_provider="openai",
            model_name="gpt-4",
            tools=["brand_system", "style_guide"],
            capabilities=["brand_strategy", "identity_design", "guidelines"],
            prompt_template="你是一个专业的品牌设计师。请根据以下任务进行品牌设计：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"品牌设计师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"品牌设计完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


def register_design_agents(manager):
    """注册设计代理"""
    manager.register_agent("uiux_designer", UIUXDesignerAgent())
    manager.register_agent("graphic_designer", GraphicDesignerAgent())
    manager.register_agent("branding", BrandingAgent())
    logger.info("设计代理注册完成")
