"""
Response models for the Company Screener API.
"""
from typing import Optional
from pydantic import BaseModel

from app.models.job import JobStatus


class JobResponse(BaseModel):
    """Response model for job status."""
    job_id: str
    status: JobStatus


class ReportResponse(BaseModel):
    """Response model for the generated company report."""
    company_overview: str
    product_business_model: str
    market_analysis: str
    competitive_landscape: str
    financial_metrics: str
    fundraising_history: str
    team_key_stakeholders: str
