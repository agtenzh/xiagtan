"""代理管理器初始化"""
from loguru import logger

from app.agents.agent_base import agent_manager
from app.agents.marketing_agents import register_marketing_agents
from app.agents.development_agents import register_development_agents
from app.agents.design_agents import register_design_agents
from app.agents.sales_agents import register_sales_agents
from app.agents.other_agents import register_other_agents


def initialize_agents():
    """初始化所有代理"""
    register_marketing_agents(agent_manager)
    register_development_agents(agent_manager)
    register_design_agents(agent_manager)
    register_sales_agents(agent_manager)
    register_other_agents(agent_manager)
    
    logger.info(f"代理初始化完成，共注册 {len(agent_manager.agents)} 个代理")
    return agent_manager
