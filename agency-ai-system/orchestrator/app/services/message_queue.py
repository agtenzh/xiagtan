"""消息队列 - 支持内存队列和RabbitMQ"""
import asyncio
from typing import Any, Callable, Dict, Optional
from abc import ABC, abstractmethod
from loguru import logger


class MessageQueue(ABC):
    """消息队列基类"""
    
    @abstractmethod
    async def publish(self, queue: str, message: Any):
        """发布消息"""
        pass
    
    @abstractmethod
    async def consume(self, queue: str, callback: Callable):
        """消费消息"""
        pass
    
    @abstractmethod
    async def get(self, queue: str) -> Optional[Any]:
        """获取消息"""
        pass
    
    @abstractmethod
    async def size(self, queue: str) -> int:
        """获取队列大小"""
        pass
    
    @abstractmethod
    async def close(self):
        """关闭连接"""
        pass


class MemoryQueue(MessageQueue):
    """内存消息队列"""
    
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        logger.info("内存消息队列初始化完成")
    
    def _get_queue(self, name: str) -> asyncio.Queue:
        if name not in self.queues:
            self.queues[name] = asyncio.Queue()
        return self.queues[name]
    
    async def publish(self, queue: str, message: Any):
        q = self._get_queue(queue)
        await q.put(message)
        logger.debug(f"消息已发布到队列 {queue}")
    
    async def consume(self, queue: str, callback: Callable):
        q = self._get_queue(queue)
        while True:
            try:
                message = await q.get()
                await callback(message)
                q.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"消费消息失败: {e}")
    
    async def get(self, queue: str) -> Optional[Any]:
        q = self._get_queue(queue)
        try:
            return q.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    async def size(self, queue: str) -> int:
        q = self._get_queue(queue)
        return q.qsize()
    
    async def close(self):
        self.queues.clear()
        logger.info("内存消息队列已关闭")


class MessageQueueManager:
    """消息队列管理器"""
    
    def __init__(self, queue_type: str = "memory"):
        self.queue_type = queue_type
        self.queue: Optional[MessageQueue] = None
    
    async def initialize(self):
        """初始化消息队列"""
        if self.queue_type == "memory":
            self.queue = MemoryQueue()
        elif self.queue_type == "rabbitmq":
            # TODO: 实现RabbitMQ
            logger.warning("RabbitMQ暂未实现，使用内存队列")
            self.queue = MemoryQueue()
        else:
            raise ValueError(f"不支持的队列类型: {self.queue_type}")
        
        logger.info(f"消息队列初始化完成: {self.queue_type}")
    
    async def publish(self, queue: str, message: Any):
        if self.queue:
            await self.queue.publish(queue, message)
    
    async def consume(self, queue: str, callback: Callable):
        if self.queue:
            await self.queue.consume(queue, callback)
    
    async def get(self, queue: str) -> Optional[Any]:
        if self.queue:
            return await self.queue.get(queue)
        return None
    
    async def size(self, queue: str) -> int:
        if self.queue:
            return await self.queue.size(queue)
        return 0
    
    async def close(self):
        if self.queue:
            await self.queue.close()


# 全局消息队列管理器
queue_manager = MessageQueueManager()
