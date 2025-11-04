"""
Scheduler Module
Handles automated data syncing and periodic tasks
"""

import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskScheduler:
    """Manage scheduled tasks for FinOps Chatbot"""

    def __init__(self):
        """Initialize the task scheduler"""
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
        self.is_running = False
        logger.info("Task Scheduler initialized")

    def start(self) -> None:
        """Start the scheduler"""
        try:
            if not self.is_running:
                self.scheduler.start()
                self.is_running = True
                logger.info("Task Scheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}")

    def stop(self) -> None:
        """Stop the scheduler"""
        try:
            if self.is_running:
                self.scheduler.shutdown()
                self.is_running = False
                logger.info("Task Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")

    def add_job(
        self,
        func: Callable,
        trigger: str = "cron",
        job_id: str = None,
        **kwargs
    ) -> Optional[str]:
        """
        Add a scheduled job
        
        Args:
            func: Function to execute
            trigger: Trigger type (cron, interval, date)
            job_id: Unique job identifier
            **kwargs: Trigger-specific arguments
        
        Returns:
            Job ID
        """
        try:
            if job_id is None:
                job_id = f"job_{len(self.jobs)}_{datetime.now().timestamp()}"

            if trigger == "cron":
                trigger_obj = CronTrigger(**kwargs)
            elif trigger == "interval":
                from apscheduler.triggers.interval import IntervalTrigger
                trigger_obj = IntervalTrigger(**kwargs)
            else:
                logger.error(f"Unknown trigger type: {trigger}")
                return None

            job = self.scheduler.add_job(
                func,
                trigger=trigger_obj,
                id=job_id,
                name=job_id,
                replace_existing=True
            )

            self.jobs[job_id] = {
                "job": job,
                "function": func.__name__,
                "trigger": trigger,
                "created_at": datetime.now().isoformat(),
            }

            logger.info(f"Job added: {job_id}")
            return job_id

        except Exception as e:
            logger.error(f"Error adding job: {str(e)}")
            return None

    def remove_job(self, job_id: str) -> bool:
        """
        Remove a scheduled job
        
        Args:
            job_id: Job identifier
        
        Returns:
            Success status
        """
        try:
            if job_id in self.jobs:
                self.scheduler.remove_job(job_id)
                del self.jobs[job_id]
                logger.info(f"Job removed: {job_id}")
                return True
            else:
                logger.warning(f"Job not found: {job_id}")
                return False

        except Exception as e:
            logger.error(f"Error removing job: {str(e)}")
            return False

    def get_jobs(self) -> Dict[str, Any]:
        """
        Get all scheduled jobs
        
        Returns:
            Dictionary of jobs
        """
        return self.jobs

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a specific job
        
        Args:
            job_id: Job identifier
        
        Returns:
            Job status dictionary
        """
        try:
            if job_id in self.jobs:
                job_info = self.jobs[job_id]
                job = job_info["job"]

                return {
                    "job_id": job_id,
                    "function": job_info["function"],
                    "trigger": job_info["trigger"],
                    "created_at": job_info["created_at"],
                    "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                }
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            return None

    def pause_job(self, job_id: str) -> bool:
        """
        Pause a scheduled job
        
        Args:
            job_id: Job identifier
        
        Returns:
            Success status
        """
        try:
            if job_id in self.jobs:
                self.scheduler.pause_job(job_id)
                logger.info(f"Job paused: {job_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error pausing job: {str(e)}")
            return False

    def resume_job(self, job_id: str) -> bool:
        """
        Resume a paused job
        
        Args:
            job_id: Job identifier
        
        Returns:
            Success status
        """
        try:
            if job_id in self.jobs:
                self.scheduler.resume_job(job_id)
                logger.info(f"Job resumed: {job_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error resuming job: {str(e)}")
            return False


class DataSyncScheduler:
    """Specialized scheduler for data synchronization"""

    def __init__(self, chatbot):
        """
        Initialize data sync scheduler
        
        Args:
            chatbot: FinOps Chatbot instance
        """
        self.chatbot = chatbot
        self.scheduler = TaskScheduler()
        self.sync_history = []
        logger.info("Data Sync Scheduler initialized")

    def start(self) -> None:
        """Start the scheduler"""
        self.scheduler.start()

    def stop(self) -> None:
        """Stop the scheduler"""
        self.scheduler.stop()

    def schedule_daily_sync(self, hour: int = 0, minute: int = 0) -> Optional[str]:
        """
        Schedule daily data sync
        
        Args:
            hour: Hour of day (0-23)
            minute: Minute of hour (0-59)
        
        Returns:
            Job ID
        """
        job_id = self.scheduler.add_job(
            self._sync_wrapper,
            trigger="cron",
            hour=hour,
            minute=minute,
            job_id="daily_sync"
        )
        return job_id

    def schedule_hourly_sync(self) -> Optional[str]:
        """
        Schedule hourly data sync
        
        Returns:
            Job ID
        """
        job_id = self.scheduler.add_job(
            self._sync_wrapper,
            trigger="interval",
            hours=1,
            job_id="hourly_sync"
        )
        return job_id

    def schedule_custom_sync(self, interval_minutes: int) -> Optional[str]:
        """
        Schedule custom interval data sync
        
        Args:
            interval_minutes: Interval in minutes
        
        Returns:
            Job ID
        """
        job_id = self.scheduler.add_job(
            self._sync_wrapper,
            trigger="interval",
            minutes=interval_minutes,
            job_id=f"custom_sync_{interval_minutes}m"
        )
        return job_id

    def _sync_wrapper(self) -> None:
        """Wrapper for sync operation with error handling"""
        try:
            logger.info("Starting scheduled data sync")
            result = self.chatbot.sync_aws_data(days=1)

            sync_record = {
                "timestamp": datetime.now().isoformat(),
                "status": result.get("status"),
                "data_points": result.get("data_points", 0),
                "insights_generated": result.get("insights_generated", 0),
            }

            self.sync_history.append(sync_record)

            # Keep only last 100 records
            if len(self.sync_history) > 100:
                self.sync_history = self.sync_history[-100:]

            logger.info(f"Scheduled sync completed: {result}")

        except Exception as e:
            logger.error(f"Error in scheduled sync: {str(e)}")
            sync_record = {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
            }
            self.sync_history.append(sync_record)

    def get_sync_history(self, limit: int = 10) -> list:
        """
        Get sync history
        
        Args:
            limit: Number of records to return
        
        Returns:
            List of sync records
        """
        return self.sync_history[-limit:]

    def get_scheduler_status(self) -> Dict[str, Any]:
        """
        Get scheduler status
        
        Returns:
            Status dictionary
        """
        return {
            "is_running": self.scheduler.is_running,
            "jobs": self.scheduler.get_jobs(),
            "sync_history_count": len(self.sync_history),
            "last_sync": self.sync_history[-1] if self.sync_history else None,
        }
