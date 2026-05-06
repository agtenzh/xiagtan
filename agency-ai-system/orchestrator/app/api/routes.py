"""API路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.models import Task, Agent, Brain, ModelProvider
from app.models.schemas import (
    TaskCreate, TaskResponse,
    AgentCreate, AgentResponse,
    BrainCreate, BrainResponse,
    ModelProviderCreate, ModelProviderResponse,
    SystemStatus
)
from app.services.audit_service import audit_service
from app.api.audit_routes import router as audit_router
from app.api.heartbeat_routes import router as heartbeat_router
from app.api.progress_routes import router as progress_router

router = APIRouter()

# 注册审计日志路由
router.include_router(audit_router)

# 注册心跳路由
router.include_router(heartbeat_router)

# 注册进度监控路由
router.include_router(progress_router)


# 健康检查
@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "0.1.0"}


# 系统状态
@router.get("/api/system/status", response_model=SystemStatus)
async def get_system_status():
    """获取系统状态"""
    import psutil
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return SystemStatus(
        cpu_usage=cpu_usage,
        memory_usage=memory.percent,
        disk_usage=disk.percent,
        active_tasks=0,
        active_agents=0,
        active_brains=0,
        uptime=0
    )


# 任务API
@router.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """创建任务"""
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        input_data=task.input_data
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # 记录审计日志
    audit_service.log_task_created(db_task.id, db_task.title)
    
    return db_task


@router.get("/api/tasks", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    """获取任务列表"""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(Task.created_at.desc()).all()


@router.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """获取任务详情"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.post("/api/tasks/{task_id}/cancel")
async def cancel_task(task_id: str, db: Session = Depends(get_db)):
    """取消任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    task.status = "cancelled"
    db.commit()
    
    # 记录审计日志
    audit_service.log_task_cancelled(task_id, task.title)
    
    return {"message": "任务已取消"}


# 代理API
@router.post("/api/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """创建代理"""
    db_agent = Agent(
        name=agent.name,
        description=agent.description,
        category=agent.category,
        model_provider=agent.model_provider,
        model_name=agent.model_name,
        tools=agent.tools,
        capabilities=agent.capabilities,
        prompt_template=agent.prompt_template
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    # 记录审计日志
    audit_service.log_agent_created(db_agent.id, db_agent.name)
    
    return db_agent


@router.get("/api/agents", response_model=List[AgentResponse])
async def list_agents(db: Session = Depends(get_db)):
    """获取代理列表"""
    # 从数据库获取代理
    db_agents = db.query(Agent).all()
    
    # 如果数据库中没有代理，返回内存中的代理
    if not db_agents:
        from app.agents.agent_base import agent_manager
        memory_agents = agent_manager.list_agents()
        
        # 将内存代理转换为数据库格式并保存
        for agent_data in memory_agents:
            db_agent = Agent(
                name=agent_data.get("name", ""),
                description=agent_data.get("description", ""),
                category=agent_data.get("category", ""),
                model_provider=agent_data.get("model", "").split("/")[0] if "/" in agent_data.get("model", "") else "",
                model_name=agent_data.get("model", "").split("/")[1] if "/" in agent_data.get("model", "") else agent_data.get("model", ""),
                tools=agent_data.get("tools", []),
                capabilities=agent_data.get("capabilities", []),
                is_active=agent_data.get("status") == "idle"
            )
            db.add(db_agent)
        
        db.commit()
        db_agents = db.query(Agent).all()
    
    return db_agents


@router.get("/api/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """获取代理详情"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="代理不存在")
    return agent


@router.put("/api/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent: AgentCreate, db: Session = Depends(get_db)):
    """更新代理"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="代理不存在")
    
    for key, value in agent.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)
    
    db.commit()
    db.refresh(db_agent)
    
    # 记录审计日志
    audit_service.log_agent_updated(agent_id, db_agent.name)
    
    return db_agent


@router.post("/api/agents/{agent_id}/toggle")
async def toggle_agent(agent_id: str, db: Session = Depends(get_db)):
    """启用/禁用代理"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="代理不存在")
    
    agent.is_active = not agent.is_active
    db.commit()
    
    # 记录审计日志
    audit_service.log_agent_toggled(agent_id, agent.name, agent.is_active)
    
    return {"message": f"代理已{'启用' if agent.is_active else '禁用'}"}


# 大脑API
@router.post("/api/brains", response_model=BrainResponse)
async def create_brain(brain: BrainCreate, db: Session = Depends(get_db)):
    """创建大脑"""
    db_brain = Brain(
        name=brain.name,
        brain_type=brain.brain_type,
        description=brain.description,
        max_concurrent_tasks=brain.max_concurrent_tasks,
        models=brain.models,
        agents=brain.agents,
        capabilities=brain.capabilities
    )
    db.add(db_brain)
    db.commit()
    db.refresh(db_brain)
    
    # 记录审计日志
    audit_service.log_brain_created(db_brain.id, db_brain.name)
    
    return db_brain


@router.get("/api/brains", response_model=List[BrainResponse])
async def list_brains(db: Session = Depends(get_db)):
    """获取大脑列表"""
    return db.query(Brain).all()


@router.get("/api/brains/{brain_id}", response_model=BrainResponse)
async def get_brain(brain_id: str, db: Session = Depends(get_db)):
    """获取大脑详情"""
    brain = db.query(Brain).filter(Brain.id == brain_id).first()
    if not brain:
        raise HTTPException(status_code=404, detail="大脑不存在")
    return brain


@router.put("/api/brains/{brain_id}", response_model=BrainResponse)
async def update_brain(brain_id: str, brain: BrainCreate, db: Session = Depends(get_db)):
    """更新大脑"""
    db_brain = db.query(Brain).filter(Brain.id == brain_id).first()
    if not db_brain:
        raise HTTPException(status_code=404, detail="大脑不存在")
    
    for key, value in brain.dict(exclude_unset=True).items():
        setattr(db_brain, key, value)
    
    db.commit()
    db.refresh(db_brain)
    
    # 记录审计日志
    audit_service.log_brain_updated(brain_id, db_brain.name)
    
    return db_brain


# 模型API
@router.post("/api/models", response_model=ModelProviderResponse)
async def create_model(model: ModelProviderCreate, db: Session = Depends(get_db)):
    """创建模型"""
    db_model = ModelProvider(
        name=model.name,
        base_url=model.base_url,
        models=model.models,
        rate_limit=model.rate_limit
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


@router.get("/api/models", response_model=List[ModelProviderResponse])
async def list_models(db: Session = Depends(get_db)):
    """获取模型列表"""
    return db.query(ModelProvider).all()


@router.put("/api/models/{model_id}", response_model=ModelProviderResponse)
async def update_model(model_id: str, model: ModelProviderCreate, db: Session = Depends(get_db)):
    """更新模型"""
    db_model = db.query(ModelProvider).filter(ModelProvider.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    for key, value in model.dict(exclude_unset=True).items():
        setattr(db_model, key, value)
    
    db.commit()
    db.refresh(db_model)
    return db_model
