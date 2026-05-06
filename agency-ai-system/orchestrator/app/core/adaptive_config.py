"""自适应配置管理"""
import psutil
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from loguru import logger


class AdaptiveConfig:
    """自适应配置管理器"""
    
    MODE_THRESHOLDS = {
        'low': {'cpu': 2, 'memory_gb': 2},
        'medium': {'cpu': 4, 'memory_gb': 4},
        'high': {'cpu': 8, 'memory_gb': 8},
        'ultra': {'cpu': 16, 'memory_gb': 16},
    }
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.current_mode = None
        self.config = None
    
    def detect_system_resources(self) -> Dict[str, Any]:
        """检测系统资源"""
        return {
            "cpu_count": psutil.cpu_count(logical=True),
            "memory_total_gb": psutil.virtual_memory().total / (1024 ** 3),
            "memory_available_gb": psutil.virtual_memory().available / (1024 ** 3),
            "disk_total_gb": psutil.disk_usage('/').total / (1024 ** 3),
            "disk_free_gb": psutil.disk_usage('/').free / (1024 ** 3),
        }
    
    def detect_optimal_mode(self) -> str:
        """检测最优配置模式"""
        resources = self.detect_system_resources()
        
        for mode in ['ultra', 'high', 'medium', 'low']:
            threshold = self.MODE_THRESHOLDS[mode]
            if (resources["cpu_count"] >= threshold['cpu'] and 
                resources["memory_total_gb"] >= threshold['memory_gb']):
                return mode
        
        return 'low'
    
    def load_config(self, mode: str = None) -> Dict[str, Any]:
        """加载配置"""
        if mode is None:
            mode = self.detect_optimal_mode()
        
        config_file = self.config_dir / f"{mode}_config.yaml"
        
        if not config_file.exists():
            logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
            return self._get_default_config(mode)
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.current_mode = mode
        self.config = config
        return config
    
    def _get_default_config(self, mode: str) -> Dict[str, Any]:
        """获取默认配置"""
        configs = {
            'low': {
                "mode": "low",
                "resources": {"max_memory": "1GB", "max_cpu": "1.5"},
                "agents": {"max_concurrent": 1, "max_loaded": 1},
                "tasks": {"max_concurrent": 1, "max_queue_size": 50},
                "database": {"type": "sqlite"},
                "queue": {"type": "memory"},
                "cache": {"type": "memory"},
            },
            'medium': {
                "mode": "medium",
                "resources": {"max_memory": "2GB", "max_cpu": "3"},
                "agents": {"max_concurrent": 2, "max_loaded": 2},
                "tasks": {"max_concurrent": 3, "max_queue_size": 100},
                "database": {"type": "sqlite"},
                "queue": {"type": "memory"},
                "cache": {"type": "memory"},
            },
            'high': {
                "mode": "high",
                "resources": {"max_memory": "6GB", "max_cpu": "6"},
                "agents": {"max_concurrent": 5, "max_loaded": 5},
                "tasks": {"max_concurrent": 10, "max_queue_size": 500},
                "database": {"type": "postgresql"},
                "queue": {"type": "rabbitmq"},
                "cache": {"type": "redis"},
            },
            'ultra': {
                "mode": "ultra",
                "resources": {"max_memory": "12GB", "max_cpu": "12"},
                "agents": {"max_concurrent": 10, "max_loaded": 10},
                "tasks": {"max_concurrent": 20, "max_queue_size": 1000},
                "database": {"type": "postgresql"},
                "queue": {"type": "rabbitmq"},
                "cache": {"type": "redis"},
            },
        }
        return configs.get(mode, configs['low'])
    
    def auto_config(self) -> Dict[str, Any]:
        """自动配置"""
        mode = self.detect_optimal_mode()
        resources = self.detect_system_resources()
        config = self.load_config(mode)
        
        logger.info(f"自动配置完成: 模式={mode}, CPU={resources['cpu_count']}核, 内存={resources['memory_total_gb']:.1f}GB")
        
        return config
    
    def get_status(self) -> Dict[str, Any]:
        """获取配置状态"""
        resources = self.detect_system_resources()
        return {
            "current_mode": self.current_mode,
            "resources": resources,
            "config": self.config
        }


# 全局自适应配置实例
adaptive_config = AdaptiveConfig()
