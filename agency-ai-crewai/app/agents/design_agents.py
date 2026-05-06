"""设计代理"""
from typing import Dict
from crewai import Agent
from app.agents.base_agent import BaseAgentFactory


class DesignAgentFactory(BaseAgentFactory):
    """设计代理工厂"""
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建设计代理"""
        return {
            "ui_designer": self._create_agent(
                role="UI Designer",
                goal="创建美观、一致的用户界面",
                backstory="""你是一个UI设计专家，擅长：
                - 设计系统开发
                - 组件库设计
                - 像素级界面设计
                - 无障碍设计""",
                tools=["file_read", "file_write"]
            ),
            "ux_architect": self._create_agent(
                role="UX Architect",
                goal="设计优秀的用户体验",
                backstory="""你是一个UX架构专家，擅长：
                - 信息架构
                - 用户流程设计
                - 交互设计
                - 线框图设计""",
                tools=["file_read", "file_write"]
            ),
            "visual_storyteller": self._create_agent(
                role="Visual Storyteller",
                goal="通过视觉元素讲述品牌故事",
                backstory="""你是一个视觉叙事专家，擅长：
                - 品牌视觉设计
                - 信息图表设计
                - 视觉内容创作
                - 品牌故事讲述""",
                tools=["file_read", "file_write"]
            )
        }
