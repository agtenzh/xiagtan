"""任务模块"""
from app.tasks.marketing_tasks import MarketingTaskFactory
from app.tasks.engineering_tasks import EngineeringTaskFactory

__all__ = [
    "MarketingTaskFactory",
    "EngineeringTaskFactory"
]
