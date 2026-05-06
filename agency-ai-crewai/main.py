"""主入口"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.api.routes import router
from app.services.brain_service import brain_service


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    
    # 设置日志
    setup_logging()
    
    # 创建应用
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI多代理系统 - CrewAI版本"
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
        await brain_service.initialize()
        
        from loguru import logger
        logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动完成")
    
    # 关闭事件
    @app.on_event("shutdown")
    async def shutdown():
        """应用关闭"""
        await brain_service.shutdown()
        
        from loguru import logger
        logger.info(f"{settings.APP_NAME} 关闭")
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
