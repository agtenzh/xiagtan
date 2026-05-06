"""工程Crew"""
from app.crews.base_crew import BaseCrew
from app.agents.engineering_agents import EngineeringAgentFactory
from app.tasks.engineering_tasks import EngineeringTaskFactory


class EngineeringCrew(BaseCrew):
    """工程团队"""
    
    def __init__(self):
        super().__init__(
            name="Engineering Crew",
            description="负责软件开发、架构设计、代码审查、DevOps"
        )
        self.agent_factory = EngineeringAgentFactory()
        self.task_factory = EngineeringTaskFactory()
        self.initialize()
