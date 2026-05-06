"""工具模块 - Agent使用的工具"""
from typing import Any, Dict
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    ScrapeWebsiteTool,
)


class ToolRegistry:
    """工具注册表"""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        # 文件工具
        self.register("file_read", FileReadTool())
        self.register("file_write", FileWriterTool())
        
        # 网络工具
        self.register("scrape_website", ScrapeWebsiteTool())
    
    def register(self, name: str, tool: Any):
        """注册工具"""
        self.tools[name] = tool
    
    def get(self, name: str) -> Any:
        """获取工具"""
        return self.tools.get(name)
    
    def get_multiple(self, names: list) -> list:
        """获取多个工具"""
        return [self.tools[name] for name in names if name in self.tools]
    
    def list_tools(self) -> list:
        """列出所有工具"""
        return list(self.tools.keys())


# 全局工具注册表
tool_registry = ToolRegistry()
