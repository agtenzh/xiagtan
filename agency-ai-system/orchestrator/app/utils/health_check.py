"""健康检查组件"""
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger


class HealthChecker:
    """健康检查器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_health(self) -> Dict[str, Any]:
        """检查系统健康状态"""
        try:
            async with self.session.get(f"{self.base_url}/api/heartbeat/health") as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"status": "error", "code": resp.status}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def check_component(self, component_id: str) -> Dict[str, Any]:
        """检查组件健康状态"""
        try:
            async with self.session.get(f"{self.base_url}/api/heartbeat/component/{component_id}") as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"status": "error", "code": resp.status}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def send_heartbeat(self, component_id: str, metadata: Dict[str, Any] = None):
        """发送心跳"""
        try:
            async with self.session.post(
                f"{self.base_url}/api/heartbeat/beat/{component_id}",
                json=metadata
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"发送心跳失败: {e}")
            return False
    
    async def send_error(self, component_id: str, error: str):
        """发送错误"""
        try:
            async with self.session.post(
                f"{self.base_url}/api/heartbeat/error/{component_id}",
                params={"error": error}
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"发送错误失败: {e}")
            return False
    
    async def register_component(
        self,
        component_id: str,
        component_type: str,
        component_name: str,
        metadata: Dict[str, Any] = None
    ):
        """注册组件"""
        try:
            async with self.session.post(
                f"{self.base_url}/api/heartbeat/register",
                params={
                    "component_id": component_id,
                    "component_type": component_type,
                    "component_name": component_name
                },
                json=metadata
            ) as resp:
                return resp.status == 200
        except Exception as e:
            logger.error(f"注册组件失败: {e}")
            return False


class HeartbeatClient:
    """心跳客户端 - 用于代理和子服务"""
    
    def __init__(
        self,
        component_id: str,
        component_type: str,
        component_name: str,
        server_url: str = "http://localhost:8000",
        heartbeat_interval: int = 10
    ):
        self.component_id = component_id
        self.component_type = component_type
        self.component_name = component_name
        self.server_url = server_url
        self.heartbeat_interval = heartbeat_interval
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self.checker: Optional[HealthChecker] = None
    
    async def start(self):
        """启动心跳客户端"""
        if self.running:
            return
        
        self.running = True
        self.checker = HealthChecker(self.server_url)
        self.checker.session = aiohttp.ClientSession()
        
        # 注册组件
        await self.checker.register_component(
            self.component_id,
            self.component_type,
            self.component_name
        )
        
        # 启动心跳循环
        self._task = asyncio.create_task(self._heartbeat_loop())
        logger.info(f"心跳客户端已启动: {self.component_id}")
    
    async def stop(self):
        """停止心跳客户端"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self.checker and self.checker.session:
            await self.checker.session.close()
        logger.info(f"心跳客户端已停止: {self.component_id}")
    
    async def _heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            try:
                await self.checker.send_heartbeat(self.component_id)
                await asyncio.sleep(self.heartbeat_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳发送失败: {e}")
                await asyncio.sleep(1)
    
    async def report_error(self, error: str):
        """报告错误"""
        if self.checker:
            await self.checker.send_error(self.component_id, error)
