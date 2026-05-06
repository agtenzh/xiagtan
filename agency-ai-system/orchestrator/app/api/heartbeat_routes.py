"""心跳API"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.services.heartbeat_service import heartbeat_service, ComponentType

router = APIRouter(prefix="/api/heartbeat", tags=["心跳检测"])


@router.get("/status", response_model=Dict[str, Any])
async def get_heartbeat_status():
    """获取所有组件心跳状态"""
    return heartbeat_service.get_all_status()


@router.get("/component/{component_id}", response_model=Dict[str, Any])
async def get_component_heartbeat(component_id: str):
    """获取指定组件心跳状态"""
    status = heartbeat_service.get_component_status(component_id)
    if not status:
        raise HTTPException(status_code=404, detail="组件不存在")
    return status


@router.post("/beat/{component_id}")
async def send_heartbeat(component_id: str, metadata: Dict[str, Any] = None):
    """发送心跳"""
    heartbeat_service.heartbeat(component_id, metadata)
    return {"status": "ok", "component_id": component_id}


@router.post("/error/{component_id}")
async def send_heartbeat_error(component_id: str, error: str):
    """发送错误心跳"""
    heartbeat_service.heartbeat_error(component_id, error)
    return {"status": "ok", "component_id": component_id}


@router.post("/register")
async def register_component(
    component_id: str,
    component_type: str,
    component_name: str,
    metadata: Dict[str, Any] = None
):
    """注册组件"""
    try:
        comp_type = ComponentType(component_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的组件类型: {component_type}")
    
    heartbeat_service.register_component(
        component_id=component_id,
        component_type=comp_type,
        component_name=component_name,
        metadata=metadata
    )
    return {"status": "ok", "component_id": component_id}


@router.delete("/unregister/{component_id}")
async def unregister_component(component_id: str):
    """注销组件"""
    heartbeat_service.unregister_component(component_id)
    return {"status": "ok", "component_id": component_id}


@router.get("/unhealthy", response_model=List[Dict[str, Any]])
async def get_unhealthy_components():
    """获取不健康的组件"""
    return heartbeat_service.get_unhealthy_components()


@router.get("/health")
async def health_check():
    """系统健康检查"""
    status = heartbeat_service.get_all_status()
    return {
        "status": status["overall_status"],
        "timestamp": status["timestamp"],
        "components": status["total_components"],
        "healthy": status["healthy"],
        "unhealthy": status["unhealthy"]
    }
