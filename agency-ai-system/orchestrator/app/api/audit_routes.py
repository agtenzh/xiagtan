"""审计日志API"""
from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from app.services.audit_service import audit_service

router = APIRouter(prefix="/api/logs", tags=["审计日志"])


@router.get("", response_model=List[Dict])
async def get_logs(
    category: Optional[str] = Query(None, description="日志类别: task, agent, brain, system"),
    action: Optional[str] = Query(None, description="操作类型: create, update, delete, execute, complete, fail"),
    level: Optional[str] = Query(None, description="日志级别: INFO, SUCCESS, WARNING, ERROR"),
    target_type: Optional[str] = Query(None, description="目标类型: task, agent, brain, model"),
    hours: Optional[int] = Query(None, description="查询最近N小时的日志"),
    limit: int = Query(100, description="返回数量", ge=1, le=500),
    offset: int = Query(0, description="偏移量", ge=0)
):
    """查询日志"""
    start_time = None
    if hours:
        start_time = datetime.utcnow() - timedelta(hours=hours)
    
    return audit_service.get_logs(
        category=category,
        action=action,
        level=level,
        target_type=target_type,
        start_time=start_time,
        limit=limit,
        offset=offset
    )


@router.get("/recent", response_model=List[Dict])
async def get_recent_logs(limit: int = Query(50, ge=1, le=200)):
    """获取最近的日志"""
    return audit_service.get_recent_logs(limit=limit)


@router.get("/category/{category}", response_model=List[Dict])
async def get_logs_by_category(category: str, limit: int = Query(50, ge=1, le=200)):
    """按类别获取日志"""
    return audit_service.get_logs_by_category(category, limit=limit)


@router.get("/errors", response_model=List[Dict])
async def get_error_logs(limit: int = Query(50, ge=1, le=200)):
    """获取错误日志"""
    return audit_service.get_error_logs(limit=limit)


@router.get("/success", response_model=List[Dict])
async def get_success_logs(limit: int = Query(50, ge=1, le=200)):
    """获取成功日志"""
    return audit_service.get_success_logs(limit=limit)


@router.get("/task/{task_id}", response_model=List[Dict])
async def get_task_history(task_id: str):
    """获取任务历史"""
    return audit_service.get_task_history(task_id)


@router.get("/agent/{agent_id}", response_model=List[Dict])
async def get_agent_history(agent_id: str):
    """获取代理历史"""
    return audit_service.get_agent_history(agent_id)


@router.get("/statistics", response_model=Dict[str, Any])
async def get_log_statistics():
    """获取日志统计"""
    return audit_service.get_statistics()


@router.get("/search", response_model=List[Dict])
async def search_logs(
    keyword: str = Query(..., description="搜索关键词"),
    limit: int = Query(50, ge=1, le=200)
):
    """搜索日志"""
    # 获取所有日志并过滤
    all_logs = audit_service.get_logs(limit=1000)
    return [
        log for log in all_logs
        if keyword.lower() in str(log.get("message", "")).lower()
        or keyword.lower() in str(log.get("target_name", "")).lower()
        or keyword.lower() in str(log.get("actor", "")).lower()
    ][:limit]


@router.get("/timeline", response_model=List[Dict])
async def get_timeline(
    hours: int = Query(24, description="时间范围（小时）"),
    limit: int = Query(100, ge=1, le=500)
):
    """获取时间线"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    return audit_service.get_logs(start_time=start_time, limit=limit)


@router.get("/summary", response_model=Dict[str, Any])
async def get_summary():
    """获取日志摘要"""
    stats = audit_service.get_statistics()
    recent_logs = audit_service.get_recent_logs(limit=10)
    error_logs = audit_service.get_error_logs(limit=5)
    
    return {
        "statistics": stats,
        "recent_logs": recent_logs,
        "recent_errors": error_logs
    }
