import time
import logging
from fastapi import BackgroundTasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sloth-jobs")

class JobManager:
    def __init__(self):
        self.tasks = {
            "cleanup": self._cleanup_task,
            "sync": self._sync_task,
        }

    def run(self, name: str, background_tasks: BackgroundTasks):
        if name not in self.tasks:
            return {"status": "error", "message": f"Job '{name}' not found"}
        
        background_tasks.add_task(self.tasks[name])
        
        return {
            "status": "accepted",
            "job": name,
            "message": "Task started in background"
        }

    def _cleanup_task(self):
        logger.info("Starting cleanup...")
        time.sleep(3)  # Імітація важкої роботи
        logger.info("Cleanup completed!")

    def _sync_task(self):
        logger.info("Starting sync protocol...")
        time.sleep(5)
        logger.info("Sync finished successfully!")