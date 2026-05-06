"""营销代理"""
from typing import Dict
from crewai import Agent
from app.agents.base_agent import BaseAgentFactory


class MarketingAgentFactory(BaseAgentFactory):
    """营销代理工厂"""
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建营销代理"""
        return {
            "content_creator": self._create_agent(
                role="Content Creator",
                goal="创建高质量的多平台内容",
                backstory="""你是一个专业的内容创作专家，擅长：
                - 编辑日历规划
                - 多格式内容创作（博客、视频脚本、社交媒体）
                - 品牌故事讲述
                - SEO优化内容""",
                tools=["web_search", "file_write"]
            ),
            "seo_specialist": self._create_agent(
                role="SEO Specialist",
                goal="优化搜索引擎排名和有机流量",
                backstory="""你是一个SEO专家，专注于：
                - 技术SEO审计
                - 内容优化
                - 链接建设
                - SERP特性优化""",
                tools=["web_search", "website_search"]
            ),
            "social_media": self._create_agent(
                role="Social Media Strategist",
                goal="制定和执行社交媒体策略",
                backstory="""你是一个社交媒体策略师，擅长：
                - 平台特定内容策略
                - 社区管理
                - 参与度优化
                - 社交聆听""",
                tools=["web_search"]
            ),
            "growth_hacker": self._create_agent(
                role="Growth Hacker",
                goal="快速增长用户和转化率",
                backstory="""你是一个增长黑客专家，擅长：
                - 快速实验
                - 病毒式传播
                - 用户获取
                - 转化优化""",
                tools=["web_search"]
            )
        }
