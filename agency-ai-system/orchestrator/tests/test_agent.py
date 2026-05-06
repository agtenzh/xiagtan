"""单元测试 - 代理测试"""
import pytest
from app.agents.agent_base import AgentManager, AgentConfig, AgentCategory
from app.agents.marketing_agents import ContentCreatorAgent, SEOExpertAgent
from app.agents.development_agents import CodeGeneratorAgent


@pytest.fixture
def agent_manager():
    return AgentManager()


@pytest.fixture
def content_agent():
    return ContentCreatorAgent()


@pytest.fixture
def code_agent():
    return CodeGeneratorAgent()


class TestAgentManager:
    """代理管理器测试"""
    
    def test_register_agent(self, agent_manager, content_agent):
        """测试注册代理"""
        agent_manager.register_agent("content_creator", content_agent)
        assert "content_creator" in agent_manager.agents
    
    def test_get_agent(self, agent_manager, content_agent):
        """测试获取代理"""
        agent_manager.register_agent("content_creator", content_agent)
        agent = agent_manager.get_agent("content_creator")
        assert agent is not None
        assert agent.config.name == "内容创作者"
    
    def test_get_nonexistent_agent(self, agent_manager):
        """测试获取不存在的代理"""
        agent = agent_manager.get_agent("nonexistent")
        assert agent is None
    
    def test_list_agents(self, agent_manager, content_agent, code_agent):
        """测试列出代理"""
        agent_manager.register_agent("content_creator", content_agent)
        agent_manager.register_agent("code_generator", code_agent)
        agents = agent_manager.list_agents()
        assert len(agents) == 2


class TestContentCreatorAgent:
    """内容创作者代理测试"""
    
    def test_config(self, content_agent):
        """测试配置"""
        assert content_agent.config.name == "内容创作者"
        assert content_agent.config.category == AgentCategory.MARKETING
    
    def test_get_prompt(self, content_agent):
        """测试获取提示词"""
        task = {"description": "创建博客文章"}
        prompt = content_agent.get_prompt(task)
        assert "创建博客文章" in prompt
    
    @pytest.mark.asyncio
    async def test_execute(self, content_agent):
        """测试执行任务"""
        task = {"id": "test-1", "title": "测试任务"}
        result = await content_agent.execute(task)
        assert result["status"] == "completed"


class TestCodeGeneratorAgent:
    """代码生成器代理测试"""
    
    def test_config(self, code_agent):
        """测试配置"""
        assert code_agent.config.name == "代码生成器"
        assert code_agent.config.category == AgentCategory.DEVELOPMENT
    
    @pytest.mark.asyncio
    async def test_execute(self, code_agent):
        """测试执行任务"""
        task = {"id": "test-2", "title": "代码生成任务"}
        result = await code_agent.execute(task)
        assert result["status"] == "completed"
