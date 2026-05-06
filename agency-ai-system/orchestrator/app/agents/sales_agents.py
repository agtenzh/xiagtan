"""销售代理"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory


class SalesStrategistAgent(BaseAgent):
    """销售策略师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="销售策略师",
            description="Sales strategy and pipeline optimization specialist",
            category=AgentCategory.SALES,
            model_provider="openai",
            model_name="gpt-4",
            tools=["crm_integration", "pipeline_analysis"],
            capabilities=["sales_strategy", "pipeline_optimization", "lead_scoring"],
            prompt_template="你是一个专业的销售策略师。请根据以下任务制定销售策略：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"销售策略师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"销售策略制定完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class AccountManagerAgent(BaseAgent):
    """客户经理代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="客户经理",
            description="Client relationship and account management specialist",
            category=AgentCategory.SALES,
            model_provider="openai",
            model_name="gpt-4",
            tools=["crm_integration", "communication"],
            capabilities=["relationship_management", "retention", "upselling"],
            prompt_template="你是一个专业的客户经理。请根据以下任务进行客户管理：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"客户经理执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"客户管理完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class NegotiatorAgent(BaseAgent):
    """谈判专家代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="谈判专家",
            description="Contract negotiation and deal closing specialist",
            category=AgentCategory.SALES,
            model_provider="openai",
            model_name="gpt-4",
            tools=["contract_analysis", "pricing"],
            capabilities=["negotiation", "deal_closing", "contract_review"],
            prompt_template="你是一个专业的谈判专家。请根据以下任务进行谈判：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"谈判专家执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"谈判完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


def register_sales_agents(manager):
    """注册销售代理"""
    manager.register_agent("sales_strategist", SalesStrategistAgent())
    manager.register_agent("account_manager", AccountManagerAgent())
    manager.register_agent("negotiator", NegotiatorAgent())
    logger.info("销售代理注册完成")
