"""销售Crew"""
from app.crews.base_crew import BaseCrew
from app.agents.sales_agents import SalesAgentFactory
from app.tasks.base_task import BaseTaskFactory
from typing import Dict, List, Any
from crewai import Task, Agent


class SalesTaskFactory(BaseTaskFactory):
    """销售任务工厂"""
    
    def create_tasks(self, agents: Dict[str, Agent], config: Dict[str, Any]) -> List[Task]:
        """创建销售任务"""
        tasks = []
        
        if "outbound_strategist" in agents:
            tasks.append(self._create_task(
                description=f"""制定外向销售策略：
                产品: {config.get('product', '未指定')}
                目标市场: {config.get('target_market', '未指定')}
                
                需要包含：
                1. ICP定义
                2. 渠道策略
                3. 消息模板
                4. 序列设计""",
                expected_output="完整的外向销售策略",
                agent=agents["outbound_strategist"]
            ))
        
        return tasks


class SalesCrew(BaseCrew):
    """销售团队"""
    
    def __init__(self):
        super().__init__(
            name="Sales Crew",
            description="负责销售策略、客户管理、管道分析"
        )
        self.agent_factory = SalesAgentFactory()
        self.task_factory = SalesTaskFactory()
        self.initialize()
