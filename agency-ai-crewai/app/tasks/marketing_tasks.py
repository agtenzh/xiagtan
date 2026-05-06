"""营销任务"""
from typing import Dict, List, Any
from crewai import Task, Agent
from app.tasks.base_task import BaseTaskFactory


class MarketingTaskFactory(BaseTaskFactory):
    """营销任务工厂"""
    
    def create_tasks(self, agents: Dict[str, Agent], config: Dict[str, Any]) -> List[Task]:
        """创建营销任务"""
        tasks = []
        
        # 内容策略任务
        if "content_creator" in agents:
            tasks.append(self._create_task(
                description=f"""为以下主题创建多平台内容策略：
                主题: {config.get('topic', '未指定')}
                平台: {', '.join(config.get('platforms', ['blog', 'twitter', 'linkedin']))}
                
                需要包含：
                1. 内容日历
                2. 各平台内容格式
                3. 发布时间表
                4. 关键指标""",
                expected_output="详细的内容策略文档，包含日历和执行计划",
                agent=agents["content_creator"]
            ))
        
        # SEO优化任务
        if "seo_specialist" in agents:
            tasks.append(self._create_task(
                description=f"""对网站进行SEO审计和优化：
                URL: {config.get('url', '未指定')}
                
                需要包含：
                1. 技术SEO检查
                2. 内容质量评估
                3. 关键词分析
                4. 竞争对手分析
                5. 优化建议""",
                expected_output="SEO审计报告，包含问题清单和优化建议",
                agent=agents["seo_specialist"]
            ))
        
        # 社交媒体任务
        if "social_media" in agents:
            tasks.append(self._create_task(
                description=f"""制定社交媒体策略：
                品牌: {config.get('brand', '未指定')}
                目标受众: {config.get('audience', '未指定')}
                
                需要包含：
                1. 平台选择策略
                2. 内容类型规划
                3. 发布频率
                4. 参与度策略""",
                expected_output="社交媒体策略文档",
                agent=agents["social_media"]
            ))
        
        return tasks
