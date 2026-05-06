"""主控Crew"""
from typing import Dict, Any
from app.crews.base_crew import BaseCrew
from app.crews.marketing_crew import MarketingCrew
from app.crews.engineering_crew import EngineeringCrew
from app.crews.design_crew import DesignCrew
from app.crews.sales_crew import SalesCrew
from loguru import logger


class MasterCrew(BaseCrew):
    """主控Crew - 协调所有专业Crew"""
    
    def __init__(self):
        super().__init__(
            name="Master Crew",
            description="负责全局协调、任务路由、负载均衡"
        )
        
        # 创建专业Crew
        self.sub_crews: Dict[str, BaseCrew] = {}
        self._initialize_sub_crews()
    
    def _initialize_sub_crews(self):
        """初始化子Crew"""
        try:
            self.sub_crews["marketing"] = MarketingCrew()
            logger.info("营销Crew初始化完成")
        except Exception as e:
            logger.warning(f"营销Crew初始化失败: {e}")
        
        try:
            self.sub_crews["engineering"] = EngineeringCrew()
            logger.info("工程Crew初始化完成")
        except Exception as e:
            logger.warning(f"工程Crew初始化失败: {e}")
        
        try:
            self.sub_crews["design"] = DesignCrew()
            logger.info("设计Crew初始化完成")
        except Exception as e:
            logger.warning(f"设计Crew初始化失败: {e}")
        
        try:
            self.sub_crews["sales"] = SalesCrew()
            logger.info("销售Crew初始化完成")
        except Exception as e:
            logger.warning(f"销售Crew初始化失败: {e}")
        
        logger.info(f"主控Crew初始化完成，共 {len(self.sub_crews)} 个子Crew")
    
    async def execute(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务 - 自动路由到合适的Crew"""
        task_type = task_config.get("type", "").lower()
        description = task_config.get("description", "").lower()
        
        # 路由到合适的Crew
        crew = self._route_task(task_type, description)
        
        if crew:
            logger.info(f"任务路由到 {crew.name}")
            return await crew.execute(task_config)
        else:
            logger.warning("没有合适的Crew处理此任务")
            return {
                "status": "error",
                "message": "没有合适的Crew处理此任务"
            }
    
    def _route_task(self, task_type: str, description: str) -> BaseCrew:
        """路由任务到合适的Crew"""
        # 营销任务
        if any(kw in task_type or kw in description for kw in [
            "营销", "marketing", "内容", "content", "seo", "社交", "social"
        ]):
            return self.sub_crews.get("marketing")
        
        # 工程任务
        if any(kw in task_type or kw in description for kw in [
            "开发", "engineering", "代码", "code", "编程", "programming"
        ]):
            return self.sub_crews.get("engineering")
        
        # 设计任务
        if any(kw in task_type or kw in description for kw in [
            "设计", "design", "ui", "ux", "界面"
        ]):
            return self.sub_crews.get("design")
        
        # 销售任务
        if any(kw in task_type or kw in description for kw in [
            "销售", "sales", "客户", "customer", "管道", "pipeline"
        ]):
            return self.sub_crews.get("sales")
        
        # 默认使用工程Crew
        return self.sub_crews.get("engineering")
    
    def get_all_status(self) -> Dict[str, Any]:
        """获取所有Crew状态"""
        status = {
            "master": self.get_status(),
            "sub_crews": {}
        }
        
        for crew_id, crew in self.sub_crews.items():
            status["sub_crews"][crew_id] = crew.get_status()
        
        return status
    
    def get_crew(self, crew_id: str) -> BaseCrew:
        """获取指定Crew"""
        return self.sub_crews.get(crew_id)
