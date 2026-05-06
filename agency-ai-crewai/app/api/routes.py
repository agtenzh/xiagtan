"""API路由"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.brain_service import brain_service
from app.models.schemas import (
    BrainCreate, BrainResponse, BrainStatus,
    AgentResponse, TaskCreate, TaskResponse,
    SystemStatus
)

router = APIRouter()


# 健康检查
@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "2.0.0"}


# 系统状态
@router.get("/api/system/status")
async def get_system_status():
    """获取系统状态"""
    return await brain_service.get_system_status()


# 大脑API
@router.get("/api/brains")
async def list_brains():
    """获取所有大脑"""
    return await brain_service.get_all_brains()


@router.post("/api/brains")
async def create_brain(brain: BrainCreate):
    """创建大脑"""
    return await brain_service.create_brain(brain.dict())


@router.get("/api/brains/{brain_id}")
async def get_brain(brain_id: str):
    """获取大脑详情"""
    brain = await brain_service.get_brain(brain_id)
    if not brain:
        raise HTTPException(status_code=404, detail="大脑不存在")
    return brain


@router.get("/api/brains/{brain_id}/status")
async def get_brain_status(brain_id: str):
    """获取大脑状态"""
    return await brain_service.get_brain_status(brain_id)


@router.post("/api/brains/{brain_id}/execute")
async def execute_task(brain_id: str, task: dict):
    """执行任务"""
    return await brain_service.execute_task(brain_id, task)


# 代理API
@router.get("/api/agents")
async def list_agents():
    """获取所有代理"""
    return await brain_service.get_all_agents()


# 任务API
@router.get("/api/tasks")
async def list_tasks(status: Optional[str] = None):
    """获取任务列表"""
    return await brain_service.get_tasks(status)


@router.post("/api/tasks")
async def create_task(task: TaskCreate):
    """创建任务 - 通过主控执行"""
    return await brain_service.execute_master_task(task.dict())
