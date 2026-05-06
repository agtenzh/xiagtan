"""应用配置"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用设置"""
    
    # 应用配置
    APP_NAME: str = "Agency AI System"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/agency.db"
    
    # 队列配置
    QUEUE_TYPE: str = "memory"  # memory, rabbitmq
    
    # 缓存配置
    CACHE_TYPE: str = "memory"  # memory, redis
    
    # 代理配置
    MAX_AGENTS: int = 2
    MAX_CONCURRENT_TASKS: int = 5
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局设置实例
settings = Settings()


def get_settings() -> Settings:
    """获取设置"""
    return settings
