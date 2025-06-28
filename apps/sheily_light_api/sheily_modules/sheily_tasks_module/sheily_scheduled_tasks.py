"""Simple task scheduler using APScheduler to orchestrate SHEILY tasks."""

import logging
from datetime import datetime
from typing import List, Dict, Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from .sheily_system_scan_task import run_system_scan

logger = logging.getLogger("sheily_tasks")

# Global background scheduler
scheduler = BackgroundScheduler()
if not scheduler.running:
    scheduler.start()


# ---------------------------------------------------------------------------
# Job helpers
# ---------------------------------------------------------------------------


def schedule_system_scan(user: str, interval_seconds: int = 3600) -> str:
    """Schedule a periodic system scan job. Returns job id."""
    job_id = f"system_scan_{user}_{interval_seconds}"
    logger.info("Scheduling system scan for user %s every %s seconds (job_id=%s)", user, interval_seconds, job_id)
    scheduler.add_job(
        func=run_system_scan,
        trigger=IntervalTrigger(seconds=interval_seconds),
        id=job_id,
        replace_existing=True,
        kwargs={"user": user},
    )
    return job_id


def schedule_custom_job(
    func,
    cron_expression: str,
    job_id: str,
    **kwargs,
) -> str:
    """Schedule an arbitrary function based on a cron expression."""
    trigger = CronTrigger.from_crontab(cron_expression)
    scheduler.add_job(func=func, trigger=trigger, id=job_id, replace_existing=True, kwargs=kwargs)
    logger.info("Scheduled job %s with cron %s", job_id, cron_expression)
    return job_id


def remove_job(job_id: str):
    scheduler.remove_job(job_id)
    logger.info("Removed job %s", job_id)


def list_jobs() -> List[Dict[str, Any]]:
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append(
            {
                "id": job.id,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger),
            }
        )
    return jobs


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
