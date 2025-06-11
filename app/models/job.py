"""
Job model for tracking report generation status.
"""
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel

from app.models.report import ReportModel


class JobStatus(str, Enum):
    """Status of a report generation job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ScreenerJob(BaseModel):
    """Model for tracking report generation jobs."""
    id: str
    status: JobStatus
    url: str
    domain: str | None = None
    report: ReportModel | None = None
    error: str | None = None


# In-memory database for jobs (replace with a proper database in production)
jobs_db: Dict[str, ScreenerJob] = {}
