"""大脑管理器"""
from typing import Dict, Optional
from loguru import logger

from app.brains.brain_base import (
    BrainNetwork, BrainConfig, BrainType,
    MasterBrain, MarketingBrain, DevelopmentBrain,
    DesignBrain, SalesBrain, AnalyticsBrain
)


class BrainManager:
    """大脑管理器 - 管理所有大脑"""
    
    def __init__(self):
        self.network = BrainNetwork()
        self.master_brain: Optional[MasterBrain] = None
        self.brains: Dict[str, any] = {}
        logger.info("大脑管理器初始化完成")
    
    async def initialize(self):
        """初始化所有大脑"""
        
        # 创建主大脑
        master_config = BrainConfig(
            brain_type=BrainType.MASTER,
            name="主大脑",
            description="负责全局协调、任务分配、负载均衡",
            max_concurrent_tasks=10,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=[],
            capabilities=["task_routing", "load_balancing", "result_integration"]
        )
        self.master_brain = MasterBrain(master_config, self.network)
        await self.network.register_brain(BrainType.MASTER.value, self.master_brain)
        
        # 创建营销大脑
        marketing_config = BrainConfig(
            brain_type=BrainType.MARKETING,
            name="营销大脑",
            description="负责营销策略、内容创作、社交媒体",
            max_concurrent_tasks=5,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=["content_creator", "seo_expert", "social_media"],
            capabilities=["content_creation", "seo", "social_media"]
        )
        marketing_brain = MarketingBrain(marketing_config, self.network)
        await self.master_brain.register_sub_brain(BrainType.MARKETING.value, marketing_brain)
        self.brains[BrainType.MARKETING.value] = marketing_brain
        
        # 创建开发大脑
        development_config = BrainConfig(
            brain_type=BrainType.DEVELOPMENT,
            name="开发大脑",
            description="负责代码生成、测试、部署",
            max_concurrent_tasks=5,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=["code_generator", "test_writer", "deployer"],
            capabilities=["code_generation", "testing", "deployment"]
        )
        development_brain = DevelopmentBrain(development_config, self.network)
        await self.master_brain.register_sub_brain(BrainType.DEVELOPMENT.value, development_brain)
        self.brains[BrainType.DEVELOPMENT.value] = development_brain
        
        # 创建设计大脑
        design_config = BrainConfig(
            brain_type=BrainType.DESIGN,
            name="设计大脑",
            description="负责UI/UX设计、视觉设计",
            max_concurrent_tasks=3,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=["ui_designer", "visual_designer"],
            capabilities=["ui_design", "visual_design"]
        )
        design_brain = DesignBrain(design_config, self.network)
        await self.master_brain.register_sub_brain(BrainType.DESIGN.value, design_brain)
        self.brains[BrainType.DESIGN.value] = design_brain
        
        # 创建销售大脑
        sales_config = BrainConfig(
            brain_type=BrainType.SALES,
            name="销售大脑",
            description="负责销售策略、客户管理",
            max_concurrent_tasks=3,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=["sales_strategist", "account_manager"],
            capabilities=["sales_strategy", "account_management"]
        )
        sales_brain = SalesBrain(sales_config, self.network)
        await self.master_brain.register_sub_brain(BrainType.SALES.value, sales_brain)
        self.brains[BrainType.SALES.value] = sales_brain
        
        # 创建分析大脑
        analytics_config = BrainConfig(
            brain_type=BrainType.ANALYTICS,
            name="分析大脑",
            description="负责数据分析、报告生成",
            max_concurrent_tasks=3,
            models=["gpt-4", "gpt-3.5-turbo"],
            agents=["data_analyst", "report_generator"],
            capabilities=["data_analysis", "report_generation"]
        )
        analytics_brain = AnalyticsBrain(analytics_config, self.network)
        await self.master_brain.register_sub_brain(BrainType.ANALYTICS.value, analytics_brain)
        self.brains[BrainType.ANALYTICS.value] = analytics_brain
        
        logger.info(f"所有大脑初始化完成，共注册 {len(self.brains) + 1} 个大脑")
    
    async def process_task(self, task: Dict) -> Dict:
        """处理任务"""
        if not self.master_brain:
            raise RuntimeError("大脑管理器未初始化")
        
        return await self.master_brain.process_task(task)
    
    def get_all_status(self) -> Dict:
        """获取所有大脑状态"""
        if not self.master_brain:
            return {"error": "大脑管理器未初始化"}
        
        return self.master_brain.get_all_status()
    
    def get_brain(self, brain_id: str):
        """获取指定大脑"""
        if brain_id == BrainType.MASTER.value:
            return self.master_brain
        return self.brains.get(brain_id)


# 全局大脑管理器实例
brain_manager = BrainManager()
