"""营销Crew"""
from app.crews.base_crew import BaseCrew
from app.agents.marketing_agents import MarketingAgentFactory
from app.tasks.marketing_tasks import MarketingTaskFactory


class MarketingCrew(BaseCrew):
    """营销团队"""
    
    def __init__(self):
        super().__init__(
            name="Marketing Crew",
            description="负责营销策略、内容创作、社交媒体、增长黑客"
        )
        self.agent_factory = MarketingAgentFactory()
        self.task_factory = MarketingTaskFactory()
        self.initialize()
