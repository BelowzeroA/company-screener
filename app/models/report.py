"""
Report model for structured company information.
"""
from pydantic import BaseModel


class ReportModel(BaseModel):
    """Model for the structured company report."""
    company_overview: str | None = None
    product_business_model: str | None = None
    market_analysis: str | None = None
    competitive_landscape: str | None = None
    financial_metrics: str | None = None
    fundraising_history: str | None = None
    team_key_stakeholders: str | None = None
