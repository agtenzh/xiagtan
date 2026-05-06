"""进度监控服务 - 定时检查子线程状态并向用户汇报"""
import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from loguru import logger


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class ThreadStatus(str, Enum):
    """线程状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class TaskProgress:
    """任务进度"""
    task_id: str
    task_name: str
    thread_id: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0-100
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreadInfo:
    """线程信息"""
    thread_id: str
    thread_name: str
    status: ThreadStatus = ThreadStatus.IDLE
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    last_heartbeat: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProgressMonitor:
    """进度监控器"""
    
    def __init__(self, report_interval: int = 60):
        """
        初始化进度监控器
        
        Args:
            report_interval: 汇报间隔（秒）
        """
        self.report_interval = report_interval
        self.tasks: Dict[str, TaskProgress] = {}
        self.threads: Dict[str, ThreadInfo] = {}
        self.running = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._report_callbacks: List[Any] = []
        logger.info(f"进度监控器初始化完成 (汇报间隔: {report_interval}s)")
    
    async def start(self):
        """启动监控"""
        if self.running:
            return
        
        self.running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("进度监控器已启动")
    
    async def stop(self):
        """停止监控"""
        self.running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("进度监控器已停止")
    
    def register_thread(self, thread_id: str, thread_name: str):
        """注册线程"""
        self.threads[thread_id] = ThreadInfo(
            thread_id=thread_id,
            thread_name=thread_name,
            last_heartbeat=time.time()
        )
        logger.info(f"线程已注册: {thread_id} ({thread_name})")
    
    def update_thread_status(self, thread_id: str, status: ThreadStatus, current_task: str = None):
        """更新线程状态"""
        if thread_id in self.threads:
            thread = self.threads[thread_id]
            thread.status = status
            thread.current_task = current_task
            thread.last_heartbeat = time.time()
    
    def register_task(self, task_id: str, task_name: str, thread_id: str):
        """注册任务"""
        self.tasks[task_id] = TaskProgress(
            task_id=task_id,
            task_name=task_name,
            thread_id=thread_id,
            start_time=time.time()
        )
        logger.info(f"任务已注册: {task_id} ({task_name}) -> 线程 {thread_id}")
    
    def update_task_progress(self, task_id: str, progress: float, details: Dict[str, Any] = None):
        """更新任务进度"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.progress = min(100, max(0, progress))
            task.status = TaskStatus.RUNNING
            if details:
                task.details.update(details)
            logger.debug(f"任务进度更新: {task_id} -> {progress:.1f}%")
    
    def complete_task(self, task_id: str, details: Dict[str, Any] = None):
        """完成任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.progress = 100
            task.end_time = time.time()
            if details:
                task.details.update(details)
            
            # 更新线程统计
            thread_id = task.thread_id
            if thread_id in self.threads:
                self.threads[thread_id].tasks_completed += 1
            
            logger.info(f"任务完成: {task_id}")
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
            task.end_time = time.time()
            task.error = error
            
            # 更新线程统计
            thread_id = task.thread_id
            if thread_id in self.threads:
                self.threads[thread_id].tasks_failed += 1
            
            logger.error(f"任务失败: {task_id} - {error}")
    
    def add_report_callback(self, callback):
        """添加汇报回调"""
        self._report_callbacks.append(callback)
    
    async def _monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                # 检查线程状态
                self._check_threads()
                
                # 生成报告
                report = self.generate_report()
                
                # 调用汇报回调
                for callback in self._report_callbacks:
                    try:
                        await callback(report)
                    except Exception as e:
                        logger.error(f"汇报回调异常: {e}")
                
                await asyncio.sleep(self.report_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"监控循环异常: {e}")
                await asyncio.sleep(1)
    
    def _check_threads(self):
        """检查线程状态"""
        current_time = time.time()
        
        for thread_id, thread in self.threads.items():
            time_since_last = current_time - thread.last_heartbeat
            
            if time_since_last > 60:  # 60秒无心跳认为离线
                if thread.status != ThreadStatus.OFFLINE:
                    thread.status = ThreadStatus.OFFLINE
                    logger.warning(f"线程离线: {thread_id}")
            elif time_since_last > 30:  # 30秒无心跳认为异常
                if thread.status == ThreadStatus.BUSY:
                    thread.status = ThreadStatus.ERROR
                    logger.warning(f"线程异常: {thread_id}")
    
    def generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        # 任务统计
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        running_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
        failed_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        pending_tasks = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        
        # 线程统计
        total_threads = len(self.threads)
        busy_threads = sum(1 for t in self.threads.values() if t.status == ThreadStatus.BUSY)
        idle_threads = sum(1 for t in self.threads.values() if t.status == ThreadStatus.IDLE)
        offline_threads = sum(1 for t in self.threads.values() if t.status == ThreadStatus.OFFLINE)
        
        # 运行中的任务详情
        running_tasks_details = []
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.RUNNING:
                running_tasks_details.append({
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "thread_id": task.thread_id,
                    "progress": task.progress,
                    "elapsed_time": time.time() - task.start_time if task.start_time else 0
                })
        
        # 最近完成的任务
        recent_completed = []
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.COMPLETED:
                recent_completed.append({
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "thread_id": task.thread_id,
                    "duration": task.end_time - task.start_time if task.end_time and task.start_time else 0
                })
        recent_completed.sort(key=lambda x: x.get("duration", 0), reverse=True)
        recent_completed = recent_completed[:5]  # 最近5个
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "running_tasks": running_tasks,
                "failed_tasks": failed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            "threads": {
                "total": total_threads,
                "busy": busy_threads,
                "idle": idle_threads,
                "offline": offline_threads
            },
            "running_tasks": running_tasks_details,
            "recent_completed": recent_completed
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "thread_id": task.thread_id,
            "status": task.status.value,
            "progress": task.progress,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "elapsed_time": time.time() - task.start_time if task.start_time else 0,
            "error": task.error,
            "details": task.details
        }
    
    def get_all_status(self) -> Dict[str, Any]:
        """获取所有状态"""
        return self.generate_report()


# 全局进度监控器实例
progress_monitor = ProgressMonitor()
