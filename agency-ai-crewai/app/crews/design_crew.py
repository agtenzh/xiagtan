"""设计Crew"""
from app.crews.base_crew import BaseCrew
from app.agents.design_agents import DesignAgentFactory
from app.tasks.base_task import BaseTaskFactory
from typing import Dict, List, Any
from crewai import Task, Agent


class DesignTaskFactory(BaseTaskFactory):
    """设计任务工厂"""
    
    def create_tasks(self, agents: Dict[str, Agent], config: Dict[str, Any]) -> List[Task]:
        """创建设计任务"""
        tasks = []
        
        if "ui_designer" in agents:
            tasks.append(self._create_task(
                description=f"""设计用户界面：
                项目: {config.get('project', '未指定')}
                需求: {config.get('requirements', '未指定')}
                
                需要包含：
                1. 设计系统
                2. 组件库
                3. 界面设计
                4. 设计规范""",
                expected_output="完整的设计文档和组件库",
                agent=agents["ui_designer"]
            ))
        
        return tasks


class DesignCrew(BaseCrew):
    """设计团队"""
    
    def __init__(self):
        super().__init__(
            name="Design Crew",
            description="负责UI/UX设计、视觉设计、品牌设计"
        )
        self.agent_factory = DesignAgentFactory()
        self.task_factory = DesignTaskFactory()
        self.initialize()
