"""进度监控API"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.services.progress_monitor import progress_monitor, TaskStatus, ThreadStatus

router = APIRouter(prefix="/api/progress", tags=["进度监控"])


@router.get("/status", response_model=Dict[str, Any])
async def get_progress_status():
    """获取所有进度状态"""
    return progress_monitor.get_all_status()


@router.get("/task/{task_id}", response_model=Dict[str, Any])
async def get_task_progress(task_id: str):
    """获取任务进度"""
    status = progress_monitor.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="任务不存在")
    return status


@router.get("/report", response_model=Dict[str, Any])
async def get_progress_report():
    """获取进度报告"""
    return progress_monitor.generate_report()


@router.post("/task/{task_id}/progress")
async def update_task_progress(task_id: str, progress: float, details: Dict[str, Any] = None):
    """更新任务进度"""
    progress_monitor.update_task_progress(task_id, progress, details)
    return {"status": "ok", "task_id": task_id, "progress": progress}


@router.post("/task/{task_id}/complete")
async def complete_task(task_id: str, details: Dict[str, Any] = None):
    """完成任务"""
    progress_monitor.complete_task(task_id, details)
    return {"status": "ok", "task_id": task_id}


@router.post("/task/{task_id}/fail")
async def fail_task(task_id: str, error: str):
    """任务失败"""
    progress_monitor.fail_task(task_id, error)
    return {"status": "ok", "task_id": task_id}


@router.post("/thread/{thread_id}/status")
async def update_thread_status(thread_id: str, status: str, current_task: str = None):
    """更新线程状态"""
    try:
        thread_status = ThreadStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的状态: {status}")
    
    progress_monitor.update_thread_status(thread_id, thread_status, current_task)
    return {"status": "ok", "thread_id": thread_id}


@router.get("/threads", response_model=Dict[str, Any])
async def get_threads_status():
    """获取所有线程状态"""
    report = progress_monitor.generate_report()
    return report["threads"]
