"""开发代理"""
import asyncio
from typing import Dict, Any
from loguru import logger

from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory


class CodeGeneratorAgent(BaseAgent):
    """代码生成器代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="代码生成器",
            description="Full-stack code generation and debugging specialist",
            category=AgentCategory.DEVELOPMENT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["file_read", "file_write", "code_execute"],
            capabilities=["code_generation", "debugging", "refactoring"],
            prompt_template="你是一个专业的代码生成专家。请根据以下任务生成高质量的代码：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"代码生成器执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"代码生成完成: {task.get('title', '未知')}",
            "agent": self.config.name,
            "code_lines": 150
        }


class TestWriterAgent(BaseAgent):
    """测试编写器代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="测试编写器",
            description="Automated test generation specialist",
            category=AgentCategory.DEVELOPMENT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["file_read", "file_write", "test_runner"],
            capabilities=["unit_testing", "integration_testing", "test_automation"],
            prompt_template="你是一个测试编写专家。请根据以下任务编写测试用例：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"测试编写器执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"测试用例编写完成: {task.get('title', '未知')}",
            "agent": self.config.name,
            "test_count": 10
        }


class DeployerAgent(BaseAgent):
    """部署专家代理"""
    
    def __init__(self):
        config = AgentConfig(
            name="部署专家",
            description="Deployment and DevOps specialist",
            category=AgentCategory.DEVELOPMENT,
            model_provider="openai",
            model_name="gpt-4",
            tools=["shell_execute", "docker_api"],
            capabilities=["deployment", "ci_cd", "containerization"],
            prompt_template="你是一个部署专家。请根据以下任务完成部署：\n\n{task_description}"
        )
        super().__init__(config)
    
    def get_prompt(self, task: Dict[str, Any]) -> str:
        return self.config.prompt_template.format(
            task_description=task.get("description", "")
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"部署专家执行任务: {task.get('title', '未知')}")
        await asyncio.sleep(1)
        return {
            "status": "completed",
            "output": f"部署完成: {task.get('title', '未知')}",
            "agent": self.config.name
        }


def register_development_agents(manager):
    """注册开发代理"""
    manager.register_agent("code_generator", CodeGeneratorAgent())
    manager.register_agent("test_writer", TestWriterAgent())
    manager.register_agent("deployer", DeployerAgent())
    logger.info("开发代理注册完成")
