"""代理基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from crewai import Agent
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.tools.registry import tool_registry


class BaseAgentFactory(ABC):
    """代理工厂基类"""
    
    def __init__(self):
        self.llm = self._create_llm()
    
    def _create_llm(self):
        """创建LLM实例"""
        if settings.OPENAI_API_KEY:
            return ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        # 可以添加其他模型支持
        raise ValueError("未配置OPENAI_API_KEY")
    
    @abstractmethod
    def create_agents(self) -> Dict[str, Agent]:
        """创建代理集合"""
        pass
    
    def _create_agent(
        self,
        role: str,
        goal: str,
        backstory: str,
        tools: List[str] = None,
        verbose: bool = True,
        allow_delegation: bool = False
    ) -> Agent:
        """创建单个代理"""
        agent_tools = []
        if tools:
            agent_tools = tool_registry.get_multiple(tools)
        
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=agent_tools,
            llm=self.llm,
            verbose=verbose,
            allow_delegation=allow_delegation,
            memory=True
        )
