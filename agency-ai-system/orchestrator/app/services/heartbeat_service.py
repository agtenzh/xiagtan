"""心跳服务 - 监控系统组件健康状态"""
import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from loguru import logger


class ComponentType(str, Enum):
    """组件类型"""
    BRAIN = "brain"
    AGENT = "agent"
    SERVICE = "service"
    DATABASE = "database"
    QUEUE = "queue"


class HealthStatus(str, Enum):
    """健康状态"""
    HEALTHY = "healthy"      # 健康
    DEGRADED = "degraded"    # 降级
    UNHEALTHY = "unhealthy"  # 不健康
    UNKNOWN = "unknown"      # 未知


@dataclass
class HeartbeatInfo:
    """心跳信息"""
    component_id: str
    component_type: ComponentType
    component_name: str
    status: HealthStatus = HealthStatus.UNKNOWN
    last_heartbeat: float = 0
    heartbeat_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class HeartbeatService:
    """心跳服务"""
    
    def __init__(self, check_interval: int = 30, timeout: int = 120):
        """
        初始化心跳服务
        
        Args:
            check_interval: 检查间隔（秒）
            timeout: 心跳超时时间（秒）
        """
        self.check_interval = check_interval
        self.timeout = timeout
        self.components: Dict[str, HeartbeatInfo] = {}
        self.running = False
        self._check_task: Optional[asyncio.Task] = None
        logger.info(f"心跳服务初始化完成 (检查间隔: {check_interval}s, 超时: {timeout}s)")
    
    async def start(self):
        """启动心跳服务"""
        if self.running:
            logger.warning("心跳服务已在运行")
            return
        
        self.running = True
        self._check_task = asyncio.create_task(self._check_loop())
        logger.info("心跳服务已启动")
    
    async def stop(self):
        """停止心跳服务"""
        self.running = False
        if self._check_task:
            self._check_task.cancel()
            try:
                await self._check_task
            except asyncio.CancelledError:
                pass
        logger.info("心跳服务已停止")
    
    def register_component(
        self,
        component_id: str,
        component_type: ComponentType,
        component_name: str,
        metadata: Dict[str, Any] = None
    ):
        """注册组件"""
        self.components[component_id] = HeartbeatInfo(
            component_id=component_id,
            component_type=component_type,
            component_name=component_name,
            status=HealthStatus.HEALTHY,  # 注册时默认健康
            last_heartbeat=time.time(),
            heartbeat_count=1,  # 注册时算一次心跳
            metadata=metadata or {}
        )
        logger.info(f"组件已注册: {component_id} ({component_name})")
    
    def unregister_component(self, component_id: str):
        """注销组件"""
        if component_id in self.components:
            del self.components[component_id]
            logger.info(f"组件已注销: {component_id}")
    
    def heartbeat(self, component_id: str, metadata: Dict[str, Any] = None):
        """接收心跳"""
        if component_id not in self.components:
            logger.warning(f"未注册的组件发送心跳: {component_id}")
            return
        
        component = self.components[component_id]
        component.last_heartbeat = time.time()
        component.heartbeat_count += 1
        component.status = HealthStatus.HEALTHY
        
        if metadata:
            component.metadata.update(metadata)
        
        logger.debug(f"心跳接收: {component_id}")
    
    def heartbeat_error(self, component_id: str, error: str):
        """接收错误心跳"""
        if component_id not in self.components:
            return
        
        component = self.components[component_id]
        component.error_count += 1
        component.last_error = error
        component.status = HealthStatus.DEGRADED
        
        logger.warning(f"组件错误: {component_id} - {error}")
    
    async def _check_loop(self):
        """检查循环"""
        while self.running:
            try:
                await self._check_components()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳检查异常: {e}")
                await asyncio.sleep(1)
    
    async def _check_components(self):
        """检查所有组件"""
        current_time = time.time()
        
        for component_id, component in self.components.items():
            time_since_last = current_time - component.last_heartbeat
            
            if time_since_last > self.timeout:
                if component.status != HealthStatus.UNHEALTHY:
                    component.status = HealthStatus.UNHEALTHY
                    logger.error(f"组件超时: {component_id} ({time_since_last:.1f}s)")
            elif time_since_last > self.timeout / 2:
                if component.status == HealthStatus.HEALTHY:
                    component.status = HealthStatus.DEGRADED
                    logger.warning(f"组件响应慢: {component_id} ({time_since_last:.1f}s)")
    
    def get_component_status(self, component_id: str) -> Optional[Dict[str, Any]]:
        """获取组件状态"""
        if component_id not in self.components:
            return None
        
        component = self.components[component_id]
        
        # 处理 component_type 可能是字符串或枚举的情况
        comp_type = component.component_type
        if isinstance(comp_type, ComponentType):
            comp_type = comp_type.value
        
        return {
            "component_id": component.component_id,
            "component_type": comp_type,
            "component_name": component.component_name,
            "status": component.status.value,
            "last_heartbeat": component.last_heartbeat,
            "heartbeat_count": component.heartbeat_count,
            "error_count": component.error_count,
            "last_error": component.last_error,
            "uptime": time.time() - component.last_heartbeat if component.last_heartbeat > 0 else 0,
            "metadata": component.metadata
        }
    
    def get_all_status(self) -> Dict[str, Any]:
        """获取所有组件状态"""
        components = {}
        healthy_count = 0
        degraded_count = 0
        unhealthy_count = 0
        
        for component_id, component in self.components.items():
            status = self.get_component_status(component_id)
            components[component_id] = status
            
            if component.status == HealthStatus.HEALTHY:
                healthy_count += 1
            elif component.status == HealthStatus.DEGRADED:
                degraded_count += 1
            elif component.status == HealthStatus.UNHEALTHY:
                unhealthy_count += 1
        
        total = len(self.components)
        overall_status = HealthStatus.HEALTHY
        
        if unhealthy_count > 0:
            overall_status = HealthStatus.UNHEALTHY
        elif degraded_count > 0:
            overall_status = HealthStatus.DEGRADED
        
        return {
            "overall_status": overall_status.value,
            "total_components": total,
            "healthy": healthy_count,
            "degraded": degraded_count,
            "unhealthy": unhealthy_count,
            "components": components,
            "check_interval": self.check_interval,
            "timeout": self.timeout,
            "timestamp": time.time()
        }
    
    def get_unhealthy_components(self) -> List[Dict[str, Any]]:
        """获取不健康的组件"""
        unhealthy = []
        for component_id, component in self.components.items():
            if component.status in [HealthStatus.UNHEALTHY, HealthStatus.DEGRADED]:
                unhealthy.append(self.get_component_status(component_id))
        return unhealthy


# 全局心跳服务实例
heartbeat_service = HeartbeatService()
