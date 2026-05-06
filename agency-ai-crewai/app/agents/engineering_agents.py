"""工程代理"""
from typing import Dict
from crewai import Agent
from app.agents.base_agent import BaseAgentFactory


class EngineeringAgentFactory(BaseAgentFactory):
    """工程代理工厂"""
    
    def create_agents(self) -> Dict[str, Agent]:
        """创建工程代理"""
        return {
            "senior_developer": self._create_agent(
                role="Senior Developer",
                goal="实现高质量的全栈代码",
                backstory="""你是一个高级全栈开发专家，擅长：
                - 现代框架集成
                - 高级CSS和动画
                - 性能优化
                - 代码审查""",
                tools=["file_read", "file_write", "code_execute"]
            ),
            "code_reviewer": self._create_agent(
                role="Code Reviewer",
                goal="提供高质量的代码审查反馈",
                backstory="""你是一个代码审查专家，专注于：
                - 正确性检查
                - 安全漏洞检测
                - 性能分析
                - 可维护性评估""",
                tools=["file_read"]
            ),
            "backend_architect": self._create_agent(
                role="Backend Architect",
                goal="设计可扩展的后端架构",
                backstory="""你是一个后端架构专家，擅长：
                - API设计
                - 数据库建模
                - 系统架构
                - 可扩展性设计""",
                tools=["file_read", "file_write"]
            ),
            "devops_automator": self._create_agent(
                role="DevOps Automator",
                goal="自动化部署和运维流程",
                backstory="""你是一个DevOps专家，擅长：
                - CI/CD流水线
                - 基础设施即代码
                - 容器编排
                - 监控和告警""",
                tools=["code_execute", "file_write"]
            ),
            "security_engineer": self._create_agent(
                role="Security Engineer",
                goal="确保系统安全性",
                backstory="""你是一个安全工程专家，擅长：
                - 安全审计
                - 漏洞评估
                - 合规检查
                - 事件响应""",
                tools=["file_read", "code_execute"]
            )
        }
