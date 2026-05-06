"""其他代理 - 产品、测试、财务等"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory


# 产品代理
class ProductManagerAgent(BaseAgent):
    """产品经理代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="产品经理",
            description="Product management and strategy specialist",
            category=AgentCategory.PRODUCT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["roadmap_planning", "user_research"],
            capabilities=["product_strategy", "roadmap_planning", "backlog_management"],
            prompt_template="你是一个专业的产品经理。请根据以下任务进行产品管理：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"产品经理执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"产品管理完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class UserResearcherAgent(BaseAgent):
    """用户研究员代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="用户研究员",
            description="User research and feedback analysis specialist",
            category=AgentCategory.PRODUCT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["user_surveys", "interview_analysis"],
            capabilities=["user_research", "feedback_analysis", "persona_development"],
            prompt_template="你是一个专业的用户研究员。请根据以下任务进行研究：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"用户研究员执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"用户研究完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


# 测试代理
class QAEngineerAgent(BaseAgent):
    """质量工程师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="质量工程师",
            description="Quality assurance and testing specialist",
            category=AgentCategory.TESTING,
            model_provider="openai",
            model_name="gpt-4",
            tools=["test_framework", "bug_tracking"],
            capabilities=["qa_testing", "test_automation", "quality_control"],
            prompt_template="你是一个专业的质量工程师。请根据以下任务进行测试：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"质量工程师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"质量测试完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class PerformanceTesterAgent(BaseAgent):
    """性能测试代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="性能测试",
            description="Performance and load testing specialist",
            category=AgentCategory.TESTING,
            model_provider="openai",
            model_name="gpt-4",
            tools=["load_testing", "performance_monitoring"],
            capabilities=["performance_testing", "load_testing"],
            prompt_template="你是一个专业的性能测试工程师。请根据以下任务进行性能测试：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"性能测试工程师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"性能测试完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


# 财务代理
class FinancialAnalystAgent(BaseAgent):
    """财务分析师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="财务分析师",
            description="Financial analysis and reporting specialist",
            category=AgentCategory.FINANCE,
            model_provider="openai",
            model_name="gpt-4",
            tools=["financial_analysis", "budgeting"],
            capabilities=["financial_analysis", "forecasting", "reporting"],
            prompt_template="你是一个专业的财务分析师。请根据以下任务进行财务分析：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"财务分析师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"财务分析完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class BudgetPlannerAgent(BaseAgent):
    """预算规划师代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="预算规划师",
            description="Budget planning and financial forecasting specialist",
            category=AgentCategory.FINANCE,
            model_provider="openai",
            model_name="gpt-4",
            tools=["budgeting", "forecasting"],
            capabilities=["budget_planning", "forecasting"],
            prompt_template="你是一个专业的预算规划师。请根据以下任务进行预算规划：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"预算规划师执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"预算规划完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


# 项目管理代理
class ProjectManagerAgent(BaseAgent):
    """项目经理代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="项目经理",
            description="Project planning and execution management specialist",
            category=AgentCategory.PROJECT_MANAGEMENT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["project_planning", "resource_management", "risk_management"],
            capabilities=["project_planning", "project_execution", "risk_management"],
            prompt_template="你是一个专业的项目经理。请根据以下任务进行项目管理：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"项目经理执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"项目管理完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


# 付费媒体代理
class PPCSpecialistAgent(BaseAgent):
    """PPC专家代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="PPC专家",
            description="Paid search and PPC campaign management specialist",
            category=AgentCategory.PAID_MEDIA,
            model_provider="openai",
            model_name="gpt-4",
            tools=["ppc_management", "campaign_optimization"],
            capabilities=["ppc_advertising", "campaign_management", "ROI_optimization"],
            prompt_template="你是一个专业的PPC专家。请根据以下任务进行PPC管理：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"PPC专家执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"PPC管理完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


class SocialAdsAgent(BaseAgent):
    """社交广告代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="社交广告",
            description="Social media advertising and campaign management specialist",
            category=AgentCategory.PAID_MEDIA,
            model_provider="openai",
            model_name="gpt-4",
            tools=["social_ads", "campaign_optimization"],
            capabilities=["social_advertising", "audience_targeting", "campaign_management"],
            prompt_template="你是一个专业的社交广告专家。请根据以下任务进行社交广告管理：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"社交广告专家执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"社交广告管理完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


def register_other_agents(manager):
    """注册其他代理"""
    # 产品代理
    manager.register_agent("product_manager", ProductManagerAgent())
    manager.register_agent("user_researcher", UserResearcherAgent())
    # 测试代理
    manager.register_agent("qa_engineer", QAEngineerAgent())
    manager.register_agent("performance_tester", PerformanceTesterAgent())
    # 财务代理
    manager.register_agent("financial_analyst", FinancialAnalystAgent())
    manager.register_agent("budget_planner", BudgetPlannerAgent())
    # 项目管理代理
    manager.register_agent("project_manager", ProjectManagerAgent())
    # 付费媒体代理
    manager.register_agent("ppc_specialist", PPCSpecialistAgent())
    manager.register_agent("social_ads", SocialAdsAgent())
    logger.info("其他代理注册完成")
