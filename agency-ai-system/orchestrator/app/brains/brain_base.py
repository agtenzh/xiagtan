"""大脑基类和多大脑架构"""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from loguru import logger


class BrainType(str, Enum):
    """大脑类型"""
    MASTER = "master"
    MARKETING = "marketing"
    DEVELOPMENT = "development"
    DESIGN = "design"
    SALES = "sales"
    ANALYTICS = "analytics"


class BrainStatus(str, Enum):
    """大脑状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class BrainMessage:
    """大脑间消息"""
    source: str
    target: str
    message_type: str  # task_request, task_result, status_update, collaboration
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class BrainConfig:
    """大脑配置"""
    brain_type: BrainType
    name: str
    description: str
    max_concurrent_tasks: int = 5
    models: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)


class BrainNetwork:
    """大脑网络 - 管理多个大脑之间的通信"""
    
    def __init__(self):
        self.brains: Dict[str, 'Brain'] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.connections: Dict[str, List[str]] = {}
        logger.info("大脑网络初始化完成")
    
    async def register_brain(self, brain_id: str, brain: 'Brain'):
        """注册大脑"""
        self.brains[brain_id] = brain
        self.connections[brain_id] = []
        logger.info(f"大脑 {brain_id} ({brain.config.name}) 已注册")
    
    async def connect_brains(self, brain1_id: str, brain2_id: str):
        """连接两个大脑"""
        if brain1_id not in self.connections:
            self.connections[brain1_id] = []
        if brain2_id not in self.connections:
            self.connections[brain2_id] = []
        
        if brain2_id not in self.connections[brain1_id]:
            self.connections[brain1_id].append(brain2_id)
        if brain1_id not in self.connections[brain2_id]:
            self.connections[brain2_id].append(brain1_id)
        
        logger.info(f"大脑 {brain1_id} 和 {brain2_id} 已连接")
    
    async def send_message(self, message: BrainMessage):
        """发送消息"""
        await self.message_queue.put(message)
        logger.debug(f"消息已发送: {message.source} -> {message.target} ({message.message_type})")
    
    async def receive_messages(self, brain_id: str) -> List[BrainMessage]:
        """接收消息"""
        messages = []
        temp_queue = asyncio.Queue()
        
        while not self.message_queue.empty():
            msg = await self.message_queue.get()
            if msg.target == brain_id:
                messages.append(msg)
            else:
                await temp_queue.put(msg)
        
        # 恢复未处理的消息
        while not temp_queue.empty():
            await self.message_queue.put(await temp_queue.get())
        
        return messages
    
    async def broadcast(self, source_id: str, message_type: str, payload: Dict[str, Any]):
        """广播消息"""
        for target_id in self.connections.get(source_id, []):
            message = BrainMessage(
                source=source_id,
                target=target_id,
                message_type=message_type,
                payload=payload
            )
            await self.send_message(message)
    
    def get_all_status(self) -> Dict[str, Any]:
        """获取所有大脑状态"""
        status = {}
        for brain_id, brain in self.brains.items():
            status[brain_id] = brain.get_status()
        return status


class Brain(ABC):
    """大脑基类"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        self.config = config
        self.network = network
        self.agents: Dict[str, Any] = {}
        self.tasks: Dict[str, Any] = {}
        self.status = BrainStatus.IDLE
        self.load = 0
        self.created_at = datetime.now()
        logger.info(f"大脑 {self.config.name} 初始化完成")
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理任务"""
        pass
    
    @abstractmethod
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择子代理"""
        pass
    
    async def delegate_task(self, task: Dict[str, Any], agent_name: str) -> Dict[str, Any]:
        """委派任务给子代理"""
        if agent_name not in self.agents:
            raise ValueError(f"代理 {agent_name} 不存在")
        
        logger.info(f"大脑 {self.config.name} 委派任务给代理 {agent_name}")
        
        # 模拟代理执行
        result = {
            "task_id": task.get("id"),
            "agent": agent_name,
            "status": "completed",
            "output": f"由 {agent_name} 处理完成"
        }
        
        return result
    
    async def collaborate(self, target_brain_id: str, task: Dict[str, Any]):
        """与其他大脑协作"""
        message = BrainMessage(
            source=self.config.brain_type.value,
            target=target_brain_id,
            message_type="collaboration_request",
            payload={"task": task}
        )
        await self.network.send_message(message)
        logger.info(f"大脑 {self.config.name} 请求与 {target_brain_id} 协作")
    
    async def update_status(self, status: BrainStatus):
        """更新状态"""
        self.status = status
        await self.network.broadcast(
            self.config.brain_type.value,
            "status_update",
            {"status": status.value, "load": self.load}
        )
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            "brain_type": self.config.brain_type.value,
            "name": self.config.name,
            "description": self.config.description,
            "status": self.status.value,
            "load": self.load,
            "agents": list(self.agents.keys()),
            "tasks": len(self.tasks),
            "max_concurrent_tasks": self.config.max_concurrent_tasks,
            "created_at": self.created_at.isoformat()
        }


class MasterBrain(Brain):
    """主大脑 - 负责全局协调"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.sub_brains: Dict[str, Brain] = {}
        logger.info("主大脑初始化完成")
    
    async def register_sub_brain(self, brain_id: str, brain: Brain):
        """注册子大脑"""
        self.sub_brains[brain_id] = brain
        await self.network.register_brain(brain_id, brain)
        await self.network.connect_brains(self.config.brain_type.value, brain_id)
        logger.info(f"子大脑 {brain_id} ({brain.config.name}) 已注册到主大脑")
    
    async def route_task(self, task: Dict[str, Any]) -> str:
        """路由任务到合适的大脑"""
        task_type = task.get("type", "").lower()
        description = task.get("description", "").lower()
        
        if any(kw in task_type or kw in description for kw in ["营销", "marketing", "内容", "seo", "社交"]):
            return BrainType.MARKETING.value
        elif any(kw in task_type or kw in description for kw in ["开发", "code", "programming", "代码", "测试"]):
            return BrainType.DEVELOPMENT.value
        elif any(kw in task_type or kw in description for kw in ["设计", "design", "ui", "ux"]):
            return BrainType.DESIGN.value
        elif any(kw in task_type or kw in description for kw in ["销售", "sales", "客户"]):
            return BrainType.SALES.value
        elif any(kw in task_type or kw in description for kw in ["分析", "analytics", "数据", "报告"]):
            return BrainType.ANALYTICS.value
        else:
            return self.config.brain_type.value
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理任务"""
        logger.info(f"主大脑接收任务: {task.get('title', '未知')}")
        
        # 路由任务
        target_brain_id = await self.route_task(task)
        
        # 如果是子大脑负责的任务，委派给子大脑
        if target_brain_id != self.config.brain_type.value and target_brain_id in self.sub_brains:
            logger.info(f"主大脑委派任务给 {target_brain_id} 大脑")
            sub_brain = self.sub_brains[target_brain_id]
            result = await sub_brain.process_task(task)
            return result
        
        # 主大脑直接处理
        logger.info("主大脑直接处理任务")
        return {
            "task_id": task.get("id"),
            "status": "completed",
            "output": "由主大脑处理完成"
        }
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择子代理"""
        return None
    
    async def load_balance(self) -> Optional[str]:
        """负载均衡 - 找到负载最低的大脑"""
        if not self.sub_brains:
            return None
        
        loads = {brain_id: brain.load for brain_id, brain in self.sub_brains.items()}
        min_load_brain = min(loads, key=loads.get)
        
        logger.info(f"负载最低的大脑: {min_load_brain} (负载: {loads[min_load_brain]})")
        return min_load_brain
    
    def get_all_status(self) -> Dict[str, Any]:
        """获取所有大脑状态"""
        status = {
            "master": self.get_status(),
            "sub_brains": {}
        }
        
        for brain_id, brain in self.sub_brains.items():
            status["sub_brains"][brain_id] = brain.get_status()
        
        return status


class MarketingBrain(Brain):
    """营销大脑"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.agents = {
            "content_creator": {"name": "内容创作者", "status": "idle"},
            "seo_expert": {"name": "SEO专家", "status": "idle"},
            "social_media": {"name": "社交媒体专家", "status": "idle"},
        }
        logger.info("营销大脑初始化完成")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理营销任务"""
        logger.info(f"营销大脑处理任务: {task.get('title', '未知')}")
        
        agent_name = await self.select_agent(task)
        result = await self.delegate_task(task, agent_name)
        
        return result
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择营销代理"""
        description = task.get("description", "").lower()
        
        if any(kw in description for kw in ["内容", "content", "文章", "博客"]):
            return "content_creator"
        elif any(kw in description for kw in ["seo", "搜索引擎", "关键词"]):
            return "seo_expert"
        elif any(kw in description for kw in ["社交", "social", "推特", "微博"]):
            return "social_media"
        else:
            return "content_creator"


class DevelopmentBrain(Brain):
    """开发大脑"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.agents = {
            "code_generator": {"name": "代码生成器", "status": "idle"},
            "test_writer": {"name": "测试编写器", "status": "idle"},
            "deployer": {"name": "部署专家", "status": "idle"},
        }
        logger.info("开发大脑初始化完成")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理开发任务"""
        logger.info(f"开发大脑处理任务: {task.get('title', '未知')}")
        
        agent_name = await self.select_agent(task)
        result = await self.delegate_task(task, agent_name)
        
        return result
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择开发代理"""
        description = task.get("description", "").lower()
        
        if any(kw in description for kw in ["代码", "code", "编程", "函数"]):
            return "code_generator"
        elif any(kw in description for kw in ["测试", "test", "单元测试"]):
            return "test_writer"
        elif any(kw in description for kw in ["部署", "deploy", "上线"]):
            return "deployer"
        else:
            return "code_generator"


class DesignBrain(Brain):
    """设计大脑"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.agents = {
            "ui_designer": {"name": "UI设计师", "status": "idle"},
            "visual_designer": {"name": "视觉设计师", "status": "idle"},
        }
        logger.info("设计大脑初始化完成")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理设计任务"""
        logger.info(f"设计大脑处理任务: {task.get('title', '未知')}")
        
        agent_name = await self.select_agent(task)
        result = await self.delegate_task(task, agent_name)
        
        return result
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择设计代理"""
        description = task.get("description", "").lower()
        
        if any(kw in description for kw in ["ui", "界面", "交互"]):
            return "ui_designer"
        else:
            return "visual_designer"


class SalesBrain(Brain):
    """销售大脑"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.agents = {
            "sales_strategist": {"name": "销售策略师", "status": "idle"},
            "account_manager": {"name": "客户经理", "status": "idle"},
        }
        logger.info("销售大脑初始化完成")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理销售任务"""
        logger.info(f"销售大脑处理任务: {task.get('title', '未知')}")
        
        agent_name = await self.select_agent(task)
        result = await self.delegate_task(task, agent_name)
        
        return result
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择销售代理"""
        description = task.get("description", "").lower()
        
        if any(kw in description for kw in ["策略", "strategy", "计划"]):
            return "sales_strategist"
        else:
            return "account_manager"


class AnalyticsBrain(Brain):
    """分析大脑"""
    
    def __init__(self, config: BrainConfig, network: BrainNetwork):
        super().__init__(config, network)
        self.agents = {
            "data_analyst": {"name": "数据分析师", "status": "idle"},
            "report_generator": {"name": "报告生成器", "status": "idle"},
        }
        logger.info("分析大脑初始化完成")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理分析任务"""
        logger.info(f"分析大脑处理任务: {task.get('title', '未知')}")
        
        agent_name = await self.select_agent(task)
        result = await self.delegate_task(task, agent_name)
        
        return result
    
    async def select_agent(self, task: Dict[str, Any]) -> str:
        """选择分析代理"""
        description = task.get("description", "").lower()
        
        if any(kw in description for kw in ["数据", "data", "分析"]):
            return "data_analyst"
        else:
            return "report_generator"
