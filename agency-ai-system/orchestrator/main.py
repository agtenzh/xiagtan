"""总控服务主入口"""
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.api.routes import router


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    
    # 设置日志
    setup_logging()
    
    # 创建应用
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI多代理系统 - 总控服务"
    )
    
    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(router)
    
    # 启动事件
    @app.on_event("startup")
    async def startup():
        """应用启动"""
        await init_db()
        
        # 初始化代理
        from app.agents.manager import initialize_agents
        initialize_agents()
        
        # 初始化预置数据
        await init_default_data()
        
        # 启动心跳服务
        from app.services.heartbeat_service import heartbeat_service
        await heartbeat_service.start()
        
        # 启动进度监控服务
        from app.services.progress_monitor import progress_monitor
        await progress_monitor.start()
        
        # 注册系统组件
        from app.services.heartbeat_service import ComponentType
        heartbeat_service.register_component(
            component_id="orchestrator",
            component_type=ComponentType.SERVICE,
            component_name="总控服务",
            metadata={"version": settings.APP_VERSION}
        )
        
        # 记录系统启动
        from app.services.audit_service import audit_service
        audit_service.log_system_startup()
        
        # 启动后台心跳任务
        asyncio.create_task(periodic_heartbeat())
        
        from loguru import logger
        logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动完成")
    
    # 关闭事件
    @app.on_event("shutdown")
    async def shutdown():
        """应用关闭"""
        # 停止心跳服务
        from app.services.heartbeat_service import heartbeat_service
        await heartbeat_service.stop()
        
        # 停止进度监控服务
        from app.services.progress_monitor import progress_monitor
        await progress_monitor.stop()
        
        from app.services.audit_service import audit_service
        audit_service.log_system_shutdown()
        
        from loguru import logger
        logger.info(f"{settings.APP_NAME} 关闭")
    
    return app


app = create_app()


async def periodic_heartbeat():
    """定期发送心跳保持组件健康状态"""
    from app.services.heartbeat_service import heartbeat_service
    from loguru import logger
    
    while True:
        try:
            heartbeat_service.heartbeat("orchestrator")
            logger.debug("发送orchestrator心跳")
        except Exception as e:
            logger.error(f"发送心跳失败: {e}")
        
        await asyncio.sleep(10)  # 每10秒发送一次心跳


async def init_default_data():
    """初始化预置数据 - 使用 agents_config.py 配置"""
    from app.core.database import SessionLocal
    from app.models.models import ModelProvider, Brain, Agent
    from loguru import logger
    from app.config.agents_config import AGENTS_CONFIG, BRAINS_CONFIG
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_models = db.query(ModelProvider).count()
        if existing_models > 0:
            logger.info("预置数据已存在，跳过初始化")
            return
        
        logger.info("初始化预置数据...")
        
        # 添加预置模型
        default_models = [
            ModelProvider(
                name="OpenAI GPT-4",
                base_url="https://api.openai.com/v1",
                models=[
                    {"name": "gpt-4", "max_tokens": 8192, "cost_per_1k_tokens": 0.03},
                    {"name": "gpt-4-turbo", "max_tokens": 128000, "cost_per_1k_tokens": 0.01},
                    {"name": "gpt-3.5-turbo", "max_tokens": 4096, "cost_per_1k_tokens": 0.002}
                ],
                rate_limit=60,
                is_active=True
            ),
            ModelProvider(
                name="Anthropic Claude",
                base_url="https://api.anthropic.com/v1",
                models=[
                    {"name": "claude-3-opus", "max_tokens": 4096, "cost_per_1k_tokens": 0.015},
                    {"name": "claude-3-sonnet", "max_tokens": 4096, "cost_per_1k_tokens": 0.003},
                    {"name": "claude-3-haiku", "max_tokens": 4096, "cost_per_1k_tokens": 0.00025}
                ],
                rate_limit=50,
                is_active=True
            ),
            ModelProvider(
                name="本地模型 (Ollama)",
                base_url="http://localhost:11434/v1",
                models=[
                    {"name": "llama3", "max_tokens": 4096, "cost_per_1k_tokens": 0},
                    {"name": "mistral", "max_tokens": 4096, "cost_per_1k_tokens": 0},
                    {"name": "codellama", "max_tokens": 4096, "cost_per_1k_tokens": 0}
                ],
                rate_limit=100,
                is_active=True
            )
        ]
        
        for model in default_models:
            db.add(model)
        
        # 从配置文件添加大脑
        for brain_id, brain_config in BRAINS_CONFIG.items():
            brain = Brain(
                name=brain_config["name"],
                brain_type=brain_config["brain_type"],
                description=brain_config["description"],
                max_concurrent_tasks=brain_config["max_concurrent_tasks"],
                models=brain_config["models"],
                agents=brain_config["agents"],
                capabilities=brain_config["capabilities"],
                is_active=True
            )
            db.add(brain)
        
        # 从配置文件添加代理
        for agent_id, agent_config in AGENTS_CONFIG.items():
            agent = Agent(
                name=agent_config["name"],
                description=agent_config["description"],
                category=agent_config["category"],
                model_provider=agent_config["model_provider"],
                model_name=agent_config["model_name"],
                tools=agent_config["tools"],
                capabilities=agent_config["capabilities"],
                prompt_template=agent_config["prompt_template"],
                is_active=True
            )
            db.add(agent)
        
        db.commit()
        logger.info(f"预置数据初始化完成: {len(default_models)} 个模型, {len(BRAINS_CONFIG)} 个大脑, {len(AGENTS_CONFIG)} 个代理")
        
    except Exception as e:
        db.rollback()
        logger.error(f"初始化预置数据失败: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
