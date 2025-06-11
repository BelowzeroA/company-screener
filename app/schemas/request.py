"""
Request models for the Company Screener API.
"""
from pydantic import BaseModel, HttpUrl


class ReportRequest(BaseModel):
    """Request model for generating a company report."""
    url: HttpUrl
