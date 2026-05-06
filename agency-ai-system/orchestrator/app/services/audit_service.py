"""审计日志服务"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from loguru import logger

from app.models.audit_log import AuditLog
from app.core.database import SessionLocal


class AuditLogService:
    """审计日志服务"""
    
    def __init__(self):
        pass
    
    def _get_db(self) -> Session:
        return SessionLocal()
    
    def log(
        self,
        level: str,
        category: str,
        action: str,
        message: str,
        target_type: str = None,
        target_id: str = None,
        target_name: str = None,
        actor: str = "system",
        details: Dict[str, Any] = None
    ):
        """记录日志"""
        db = self._get_db()
        try:
            audit_log = AuditLog(
                level=level,
                category=category,
                action=action,
                target_type=target_type,
                target_id=target_id,
                target_name=target_name,
                actor=actor,
                details=details,
                message=message
            )
            db.add(audit_log)
            db.commit()
            logger.debug(f"[审计日志] {category}/{action}: {message}")
        except Exception as e:
            db.rollback()
            logger.error(f"记录审计日志失败: {e}")
        finally:
            db.close()
    
    def log_info(self, category: str, action: str, message: str, **kwargs):
        """记录信息日志"""
        self.log("INFO", category, action, message, **kwargs)
    
    def log_success(self, category: str, action: str, message: str, **kwargs):
        """记录成功日志"""
        self.log("SUCCESS", category, action, message, **kwargs)
    
    def log_warning(self, category: str, action: str, message: str, **kwargs):
        """记录警告日志"""
        self.log("WARNING", category, action, message, **kwargs)
    
    def log_error(self, category: str, action: str, message: str, **kwargs):
        """记录错误日志"""
        self.log("ERROR", category, action, message, **kwargs)
    
    # 任务相关日志
    def log_task_created(self, task_id: str, task_title: str):
        self.log_success("task", "create", f"任务创建: {task_title}", 
                        target_type="task", target_id=task_id, target_name=task_title)
    
    def log_task_started(self, task_id: str, task_title: str, agent_name: str):
        self.log_info("task", "start", f"任务开始执行: {task_title} (代理: {agent_name})",
                     target_type="task", target_id=task_id, target_name=task_title, actor=agent_name)
    
    def log_task_completed(self, task_id: str, task_title: str, duration: float):
        self.log_success("task", "complete", f"任务完成: {task_title} (耗时: {duration:.1f}秒)",
                        target_type="task", target_id=task_id, target_name=task_title)
    
    def log_task_failed(self, task_id: str, task_title: str, error: str):
        self.log_error("task", "fail", f"任务失败: {task_title} (错误: {error})",
                      target_type="task", target_id=task_id, target_name=task_title)
    
    def log_task_cancelled(self, task_id: str, task_title: str):
        self.log_warning("task", "cancel", f"任务取消: {task_title}",
                        target_type="task", target_id=task_id, target_name=task_title)
    
    # 代理相关日志
    def log_agent_created(self, agent_id: str, agent_name: str):
        self.log_success("agent", "create", f"代理创建: {agent_name}",
                        target_type="agent", target_id=agent_id, target_name=agent_name)
    
    def log_agent_updated(self, agent_id: str, agent_name: str):
        self.log_info("agent", "update", f"代理更新: {agent_name}",
                     target_type="agent", target_id=agent_id, target_name=agent_name)
    
    def log_agent_toggled(self, agent_id: str, agent_name: str, enabled: bool):
        action = "启用" if enabled else "禁用"
        self.log_info("agent", "toggle", f"代理{action}: {agent_name}",
                     target_type="agent", target_id=agent_id, target_name=agent_name)
    
    def log_agent_error(self, agent_id: str, agent_name: str, error: str):
        self.log_error("agent", "error", f"代理错误: {agent_name} ({error})",
                      target_type="agent", target_id=agent_id, target_name=agent_name)
    
    # 大脑相关日志
    def log_brain_created(self, brain_id: str, brain_name: str):
        self.log_success("brain", "create", f"大脑创建: {brain_name}",
                        target_type="brain", target_id=brain_id, target_name=brain_name)
    
    def log_brain_updated(self, brain_id: str, brain_name: str):
        self.log_info("brain", "update", f"大脑更新: {brain_name}",
                     target_type="brain", target_id=brain_id, target_name=brain_name)
    
    def log_brain_task_routed(self, brain_name: str, task_title: str):
        self.log_info("brain", "route", f"任务路由到 {brain_name}: {task_title}",
                     actor=brain_name)
    
    # 系统相关日志
    def log_system_startup(self):
        self.log_success("system", "startup", "系统启动")
    
    def log_system_shutdown(self):
        self.log_info("system", "shutdown", "系统关闭")
    
    def log_config_changed(self, config_type: str, details: str):
        self.log_info("system", "config", f"配置变更: {config_type} - {details}")
    
    def log_version_released(self, version: str):
        self.log_success("system", "release", f"版本发布: {version}")
    
    # 查询日志
    def get_logs(
        self,
        category: Optional[str] = None,
        action: Optional[str] = None,
        level: Optional[str] = None,
        target_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """查询日志"""
        db = self._get_db()
        try:
            query = db.query(AuditLog)
            
            if category:
                query = query.filter(AuditLog.category == category)
            if action:
                query = query.filter(AuditLog.action == action)
            if level:
                query = query.filter(AuditLog.level == level)
            if target_type:
                query = query.filter(AuditLog.target_type == target_type)
            if start_time:
                query = query.filter(AuditLog.timestamp >= start_time)
            if end_time:
                query = query.filter(AuditLog.timestamp <= end_time)
            
            query = query.order_by(desc(AuditLog.timestamp))
            query = query.offset(offset).limit(limit)
            
            return [log.to_dict() for log in query.all()]
        finally:
            db.close()
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """获取最近的日志"""
        return self.get_logs(limit=limit)
    
    def get_logs_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """按类别获取日志"""
        return self.get_logs(category=category, limit=limit)
    
    def get_logs_by_target(self, target_type: str, target_id: str) -> List[Dict]:
        """获取特定目标的日志"""
        return self.get_logs(target_type=target_type, limit=100)
    
    def get_task_history(self, task_id: str) -> List[Dict]:
        """获取任务历史"""
        return self.get_logs(target_type="task", limit=100)
    
    def get_agent_history(self, agent_id: str) -> List[Dict]:
        """获取代理历史"""
        return self.get_logs(target_type="agent", limit=100)
    
    def get_error_logs(self, limit: int = 50) -> List[Dict]:
        """获取错误日志"""
        return self.get_logs(level="ERROR", limit=limit)
    
    def get_success_logs(self, limit: int = 50) -> List[Dict]:
        """获取成功日志"""
        return self.get_logs(level="SUCCESS", limit=limit)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取日志统计"""
        db = self._get_db()
        try:
            total = db.query(AuditLog).count()
            
            # 按类别统计
            categories = {}
            for cat in ["task", "agent", "brain", "system"]:
                count = db.query(AuditLog).filter(AuditLog.category == cat).count()
                categories[cat] = count
            
            # 按级别统计
            levels = {}
            for lvl in ["INFO", "SUCCESS", "WARNING", "ERROR"]:
                count = db.query(AuditLog).filter(AuditLog.level == lvl).count()
                levels[lvl] = count
            
            # 今日统计
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_count = db.query(AuditLog).filter(AuditLog.timestamp >= today).count()
            
            return {
                "total": total,
                "categories": categories,
                "levels": levels,
                "today": today_count
            }
        finally:
            db.close()


# 全局审计日志服务
audit_service = AuditLogService()
