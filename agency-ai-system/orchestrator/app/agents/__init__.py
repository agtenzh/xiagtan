"""代理模块"""
from app.agents.agent_base import BaseAgent, AgentConfig, AgentCategory, AgentStatus, AgentManager, agent_manager
from app.agents.marketing_agents import register_marketing_agents
from app.agents.development_agents import register_development_agents
from app.agents.design_agents import register_design_agents
from app.agents.sales_agents import register_sales_agents
from app.agents.other_agents import register_other_agents

__all__ = [
    "BaseAgent",
    "AgentConfig", 
    "AgentCategory",
    "AgentStatus",
    "AgentManager",
    "agent_manager",
    "register_marketing_agents",
    "register_development_agents",
    "register_design_agents",
    "register_sales_agents",
    "register_other_agents"
]
