"""工程任务"""
from typing import Dict, List, Any
from crewai import Task, Agent
from app.tasks.base_task import BaseTaskFactory


class EngineeringTaskFactory(BaseTaskFactory):
    """工程任务工厂"""
    
    def create_tasks(self, agents: Dict[str, Agent], config: Dict[str, Any]) -> List[Task]:
        """创建工程任务"""
        tasks = []
        
        # 代码生成任务
        if "senior_developer" in agents:
            tasks.append(self._create_task(
                description=f"""根据需求生成代码：
                需求: {config.get('requirements', '未指定')}
                技术栈: {config.get('tech_stack', 'Python/FastAPI')}
                
                需要包含：
                1. 代码实现
                2. 单元测试
                3. 文档注释
                4. 使用示例""",
                expected_output="完整的代码实现，包含测试和文档",
                agent=agents["senior_developer"]
            ))
        
        # 代码审查任务
        if "code_reviewer" in agents:
            tasks.append(self._create_task(
                description=f"""审查代码：
                代码路径: {config.get('code_path', '未指定')}
                
                需要检查：
                1. 正确性
                2. 安全性
                3. 性能
                4. 可维护性""",
                expected_output="代码审查报告，包含问题清单和改进建议",
                agent=agents["code_reviewer"]
            ))
        
        # 架构设计任务
        if "backend_architect" in agents:
            tasks.append(self._create_task(
                description=f"""设计后端架构：
                项目: {config.get('project', '未指定')}
                需求: {config.get('requirements', '未指定')}
                
                需要包含：
                1. 系统架构图
                2. API设计
                3. 数据库设计
                4. 部署方案""",
                expected_output="完整的架构设计文档",
                agent=agents["backend_architect"]
            ))
        
        return tasks
