from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sheily_modules.sheily_tasks_module.sheily_system_scan_task import run_system_scan
from sheily_modules.sheily_tasks_module import sheily_scheduled_tasks as scheduler

router = APIRouter(prefix="/tasks", tags=["tasks"])


class ScanRequest(BaseModel):
    user: str
    task: str = "scan"


@router.post("/run")
def run_task(req: ScanRequest):
    return run_system_scan(req.user, req.task)


class ScheduleRequest(BaseModel):
    user: str
    interval_seconds: int = 3600


@router.post("/schedule")
def schedule_scan(req: ScheduleRequest):
    job_id = scheduler.schedule_system_scan(req.user, req.interval_seconds)
    return {"job_id": job_id}


@router.get("/jobs")
def list_jobs():
    return scheduler.list_jobs()


@router.delete("/jobs/{job_id}")
def cancel_job(job_id: str):
    try:
        scheduler.remove_job(job_id)
        return {"detail": "job removed"}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))
