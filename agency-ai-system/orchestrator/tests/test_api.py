"""单元测试 - API测试"""
import pytest
from httpx import AsyncClient
from main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestHealthAPI:
    """健康检查API测试"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """测试健康检查"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestTaskAPI:
    """任务API测试"""
    
    @pytest.mark.asyncio
    async def test_create_task(self, client):
        """测试创建任务"""
        task_data = {
            "title": "测试任务",
            "description": "这是一个测试任务",
            "priority": 5
        }
        response = await client.post("/api/tasks", json=task_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试任务"
    
    @pytest.mark.asyncio
    async def test_list_tasks(self, client):
        """测试任务列表"""
        response = await client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestAgentAPI:
    """代理API测试"""
    
    @pytest.mark.asyncio
    async def test_list_agents(self, client):
        """测试代理列表"""
        response = await client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestBrainAPI:
    """大脑API测试"""
    
    @pytest.mark.asyncio
    async def test_list_brains(self, client):
        """测试大脑列表"""
        response = await client.get("/api/brains")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestHeartbeatAPI:
    """心跳API测试"""
    
    @pytest.mark.asyncio
    async def test_heartbeat_status(self, client):
        """测试心跳状态"""
        response = await client.get("/api/heartbeat/status")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """测试健康检查"""
        response = await client.get("/api/heartbeat/health")
        assert response.status_code == 200


class TestProgressAPI:
    """进度API测试"""
    
    @pytest.mark.asyncio
    async def test_progress_status(self, client):
        """测试进度状态"""
        response = await client.get("/api/progress/status")
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_progress_report(self, client):
        """测试进度报告"""
        response = await client.get("/api/progress/report")
        assert response.status_code == 200
