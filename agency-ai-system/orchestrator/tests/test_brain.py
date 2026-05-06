"""单元测试 - 大脑测试"""
import pytest
import asyncio
from app.brains.brain_base import (
    BrainNetwork, BrainConfig, BrainType,
    MasterBrain, MarketingBrain, DevelopmentBrain,
    DesignBrain, SalesBrain, AnalyticsBrain
)


@pytest.fixture
def network():
    return BrainNetwork()


@pytest.fixture
def master_brain(network):
    config = BrainConfig(
        brain_type=BrainType.MASTER,
        name="主大脑",
        description="测试主大脑",
        max_concurrent_tasks=5
    )
    return MasterBrain(config, network)


@pytest.fixture
def marketing_brain(network):
    config = BrainConfig(
        brain_type=BrainType.MARKETING,
        name="营销大脑",
        description="测试营销大脑",
        max_concurrent_tasks=3
    )
    return MarketingBrain(config, network)


class TestBrainNetwork:
    """大脑网络测试"""
    
    @pytest.mark.asyncio
    async def test_register_brain(self, network, master_brain):
        """测试注册大脑"""
        await network.register_brain("master", master_brain)
        assert "master" in network.brains
    
    @pytest.mark.asyncio
    async def test_connect_brains(self, network, master_brain, marketing_brain):
        """测试连接大脑"""
        await network.register_brain("master", master_brain)
        await network.register_brain("marketing", marketing_brain)
        await network.connect_brains("master", "marketing")
        assert "marketing" in network.connections["master"]
        assert "master" in network.connections["marketing"]


class TestMasterBrain:
    """主大脑测试"""
    
    @pytest.mark.asyncio
    async def test_route_marketing_task(self, master_brain):
        """测试路由营销任务"""
        task = {"type": "marketing", "description": "创建营销内容"}
        target = await master_brain.route_task(task)
        assert target == BrainType.MARKETING.value
    
    @pytest.mark.asyncio
    async def test_route_development_task(self, master_brain):
        """测试路由开发任务"""
        task = {"type": "development", "description": "编写代码"}
        target = await master_brain.route_task(task)
        assert target == BrainType.DEVELOPMENT.value
    
    @pytest.mark.asyncio
    async def test_process_task(self, master_brain):
        """测试处理任务"""
        task = {"id": "test-1", "title": "测试任务", "type": "unknown"}
        result = await master_brain.process_task(task)
        assert result["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_get_status(self, master_brain):
        """测试获取状态"""
        status = master_brain.get_status()
        assert status["brain_type"] == BrainType.MASTER.value
        assert status["name"] == "主大脑"


class TestMarketingBrain:
    """营销大脑测试"""
    
    @pytest.mark.asyncio
    async def test_select_content_agent(self, marketing_brain):
        """测试选择内容代理"""
        task = {"description": "创建博客内容"}
        agent = await marketing_brain.select_agent(task)
        assert agent == "content_creator"
    
    @pytest.mark.asyncio
    async def test_select_seo_agent(self, marketing_brain):
        """测试选择SEO代理"""
        task = {"description": "SEO优化"}
        agent = await marketing_brain.select_agent(task)
        assert agent == "seo_expert"
    
    @pytest.mark.asyncio
    async def test_process_task(self, marketing_brain):
        """测试处理任务"""
        task = {"id": "test-2", "title": "营销任务", "description": "创建内容"}
        result = await marketing_brain.process_task(task)
        assert result["status"] == "completed"
