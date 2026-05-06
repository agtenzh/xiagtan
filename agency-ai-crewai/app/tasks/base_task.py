"""任务基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from crewai import Task, Agent


class BaseTaskFactory(ABC):
    """任务工厂基类"""
    
    @abstractmethod
    def create_tasks(self, agents: Dict[str, Agent], config: Dict[str, Any]) -> List[Task]:
        """创建任务列表"""
        pass
    
    def _create_task(
        self,
        description: str,
        expected_output: str,
        agent: Agent,
        tools: List[str] = None,
        async_execution: bool = False,
        output_file: str = None
    ) -> Task:
        """创建单个任务"""
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            async_execution=async_execution,
            output_file=output_file
        )
