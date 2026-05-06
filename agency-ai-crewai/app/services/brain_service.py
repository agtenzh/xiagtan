"""大脑服务"""
from typing import Dict, List, Optional, Any
from app.crews.master_crew import MasterCrew
from app.models.models import Brain, Agent, Task
from app.core.database import SessionLocal
from loguru import logger
import time


class BrainService:
    """大脑服务"""
    
    def __init__(self):
        self.master_crew: Optional[MasterCrew] = None
        self.start_time = time.time()
    
    async def initialize(self):
        """初始化大脑服务"""
        logger.info("初始化大脑服务...")
        self.master_crew = MasterCrew()
        logger.info("大脑服务初始化完成")
    
    async def shutdown(self):
        """关闭服务"""
        logger.info("关闭大脑服务...")
    
    async def create_brain(self, brain_data: dict) -> dict:
        """创建大脑"""
        db = SessionLocal()
        try:
            brain = Brain(
                name=brain_data["name"],
                brain_type=brain_data["brain_type"],
                description=brain_data.get("description"),
                max_concurrent_tasks=brain_data.get("max_concurrent_tasks", 5),
                models=brain_data.get("models"),
                agents=brain_data.get("agents"),
                capabilities=brain_data.get("capabilities")
            )
            db.add(brain)
            db.commit()
            db.refresh(brain)
            
            logger.info(f"大脑创建成功: {brain.name}")
            return self._brain_to_dict(brain)
        finally:
            db.close()
    
    async def get_all_brains(self) -> List[dict]:
        """获取所有大脑"""
        db = SessionLocal()
        try:
            brains = db.query(Brain).all()
            return [self._brain_to_dict(b) for b in brains]
        finally:
            db.close()
    
    async def get_brain(self, brain_id: str) -> Optional[dict]:
        """获取大脑详情"""
        db = SessionLocal()
        try:
            brain = db.query(Brain).filter(Brain.id == brain_id).first()
            if brain:
                return self._brain_to_dict(brain)
            return None
        finally:
            db.close()
    
    async def get_brain_status(self, brain_id: str) -> dict:
        """获取大脑状态"""
        brain = await self.get_brain(brain_id)
        if not brain:
            return {"error": "大脑不存在"}
        
        # 获取Crew状态
        crew_status = {}
        if self.master_crew:
            all_status = self.master_crew.get_all_status()
            crew_status = all_status.get("sub_crews", {}).get(brain["brain_type"], {})
        
        return {
            "brain_id": brain_id,
            "name": brain["name"],
            "status": "ready",
            "agents": len(brain.get("agents", [])),
            "tasks_completed": brain.get("tasks_completed", 0),
            "crew_status": crew_status
        }
    
    async def execute_task(self, brain_id: str, task_config: dict) -> dict:
        """执行任务"""
        brain = await self.get_brain(brain_id)
        if not brain:
            return {"status": "error", "message": "大脑不存在"}
        
        # 获取对应的Crew
        crew = None
        if self.master_crew:
            crew = self.master_crew.get_crew(brain["brain_type"])
        
        if not crew:
            return {"status": "error", "message": "Crew不存在"}
        
        # 执行任务
        result = await crew.execute(task_config)
        
        # 记录任务
        await self._record_task(brain_id, task_config, result)
        
        return result
    
    async def execute_master_task(self, task_config: dict) -> dict:
        """通过主控执行任务"""
        if not self.master_crew:
            return {"status": "error", "message": "主控Crew未初始化"}
        
        return await self.master_crew.execute(task_config)
    
    async def get_all_agents(self) -> List[dict]:
        """获取所有代理"""
        db = SessionLocal()
        try:
            agents = db.query(Agent).all()
            return [self._agent_to_dict(a) for a in agents]
        finally:
            db.close()
    
    async def get_tasks(self, status: Optional[str] = None) -> List[dict]:
        """获取任务列表"""
        db = SessionLocal()
        try:
            query = db.query(Task)
            if status:
                query = query.filter(Task.status == status)
            tasks = query.order_by(Task.created_at.desc()).all()
            return [self._task_to_dict(t) for t in tasks]
        finally:
            db.close()
    
    async def get_system_status(self) -> dict:
        """获取系统状态"""
        import psutil
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 获取Crew状态
        crew_status = {}
        if self.master_crew:
            crew_status = self.master_crew.get_all_status()
        
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "active_brains": len(crew_status.get("sub_crews", {})),
            "active_agents": sum(
                s.get("agents", 0) 
                for s in crew_status.get("sub_crews", {}).values()
            ),
            "running_tasks": 0,
            "completed_tasks": sum(
                s.get("completed_tasks", 0) 
                for s in crew_status.get("sub_crews", {}).values()
            ),
            "uptime": time.time() - self.start_time,
            "crew_status": crew_status
        }
    
    async def _record_task(self, brain_id: str, task_config: dict, result: dict):
        """记录任务"""
        db = SessionLocal()
        try:
            task = Task(
                title=task_config.get("title", "未命名任务"),
                description=task_config.get("description", ""),
                status=result.get("status", "unknown"),
                brain_id=brain_id,
                input_data=task_config,
                output_data=result,
                execution_time_ms=result.get("execution_time_ms")
            )
            db.add(task)
            db.commit()
        finally:
            db.close()
    
    def _brain_to_dict(self, brain: Brain) -> dict:
        """转换为字典"""
        return {
            "id": brain.id,
            "name": brain.name,
            "brain_type": brain.brain_type,
            "description": brain.description,
            "max_concurrent_tasks": brain.max_concurrent_tasks,
            "models": brain.models,
            "agents": brain.agents,
            "capabilities": brain.capabilities,
            "is_active": brain.is_active,
            "tasks_completed": brain.tasks_completed,
            "created_at": brain.created_at.isoformat() if brain.created_at else None
        }
    
    def _agent_to_dict(self, agent: Agent) -> dict:
        """转换为字典"""
        return {
            "id": agent.id,
            "name": agent.name,
            "role": agent.role,
            "goal": agent.goal,
            "backstory": agent.backstory,
            "category": agent.category,
            "model_provider": agent.model_provider,
            "model_name": agent.model_name,
            "tools": agent.tools,
            "capabilities": agent.capabilities,
            "is_active": agent.is_active,
            "tasks_completed": agent.tasks_completed,
            "created_at": agent.created_at.isoformat() if agent.created_at else None
        }
    
    def _task_to_dict(self, task: Task) -> dict:
        """转换为字典"""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "brain_id": task.brain_id,
            "agent_id": task.agent_id,
            "input_data": task.input_data,
            "output_data": task.output_data,
            "error_message": task.error_message,
            "execution_time_ms": task.execution_time_ms,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }


# 全局大脑服务实例
brain_service = BrainService()
