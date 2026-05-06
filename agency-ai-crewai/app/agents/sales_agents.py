"""销售代理"""
from typing import Dict
from crewai import Agent
from app.agents.base_agent import BaseAgentFactory


class SalesAgentFactory(BaseAgentFactory):
    """销售代理工厂"""
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建销售代理"""
        return {
            "outbound_strategist": self._create_agent(
                role="Outbound Strategist",
                goal="设计和执行外向销售策略",
                backstory="""你是一个外向销售策略专家，擅长：
                - 信号驱动的销售
                - 多渠道序列设计
                - ICP定义
                - 管道建设""",
                tools=["web_search", "file_write"]
            ),
            "deal_strategist": self._create_agent(
                role="Deal Strategist",
                goal="优化交易策略和赢率",
                backstory="""你是一个交易策略专家，擅长：
                - MEDDPICC资格认证
                - 竞争定位
                - 赢率规划
                - 谈判策略""",
                tools=["web_search"]
            ),
            "sales_coach": self._create_agent(
                role="Sales Coach",
                goal="提升销售团队技能",
                backstory="""你是一个销售教练，擅长：
                - 销售技能培训
                - 通话 coaching
                - 管道审查
                - 代表发展""",
                tools=["file_read", "file_write"]
            )
        }
