"""代理池服务主入口"""
import uvicorn
from fastapi import FastAPI
from loguru import logger


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    
    app = FastAPI(
        title="Agency AI - Agent Worker",
        version="0.1.0",
        description="AI多代理系统 - 代理池服务"
    )
    
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {"status": "healthy", "version": "0.1.0"}
    
    @app.on_event("startup")
    async def startup():
        """应用启动"""
        logger.info("代理池服务启动完成")
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
