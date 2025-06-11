"""
Main report generator that orchestrates the data collection and report generation process.
"""
import logging
from typing import Dict, Any, List
import asyncio

from app.data_sources.openai_websearch import OpenaiWebSearch
from app.data_sources.search_sources import SerperDataSource, PerplexityDataSource
from app.data_sources.scraper_sources import ScraperAPIDataSource
from app.data_sources.linkedin_source import CoreSignalDataSource
from app.data_sources.funding_source import TracxnDataSource
from app.models.job import Job, JobStatus, jobs_db
from app.models.report import Report
from app.utils.url_parser import extract_company_name_from_url
from app.processors.llm_processor import LLMProcessor


class ReportGenerator:
    """Main class for generating company reports."""

    def __init__(self):
        """Initialize the report generator with necessary data sources."""
        self.serper_source = SerperDataSource()
        self.web_search = OpenaiWebSearch(self.logger, self.llm)
        self.perplexity_source = PerplexityDataSource()
        self.scraper_source = ScraperAPIDataSource()
        self.linkedin_source = CoreSignalDataSource()
        self.tracxn_source = TracxnDataSource()
        self.llm_processor = LLMProcessor()
        self.logger = logging.getLogger(__name__)

    async def generate_report_async(self, job_id: str, url: str) -> None:
        """
        Generate a company report asynchronously.

        Args:
            job_id: ID of the job
            url: Company URL to analyze
        """
        try:
            # Update job status to processing
            job = jobs_db[job_id]
            job.status = JobStatus.PROCESSING

            # Extract company name from URL
            company_name = extract_company_name_from_url(url)
            self.logger.info(f"Generating report for {company_name} ({url}), job_id: {job_id}")

            serper_data = await self.serper_source.fetch_data(company_name, url)
            # Collect data from all sources concurrently
            tasks = [
                self.serper_source.fetch_data(company_name, url),
                self.perplexity_source.fetch_data(company_name, url),
                self.scraper_source.fetch_data(company_name, url),
                self.linkedin_source.fetch_data(company_name, url),
                self.tracxn_source.fetch_data(company_name, url)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine all data into a structured format
            raw_data = {
                "company_name": company_name,
                "url": url,
                "search_data": self._safe_extract(results, 0),
                "research_data": self._safe_extract(results, 1),
                "website_data": self._safe_extract(results, 2),
                "linkedin_data": self._safe_extract(results, 3),
                "funding_data": self._safe_extract(results, 4)
            }

            # Generate each report section using the LLM processor
            report = await self._generate_report_sections(raw_data)

            # Update job with completed report
            job.report = report
            job.status = JobStatus.COMPLETED
            jobs_db[job_id] = job

            self.logger.info(f"Report generation completed for job {job_id}")

        except Exception as e:
            self.logger.error(f"Error generating report for job {job_id}: {str(e)}")
            # Update job status to failed
            if job_id in jobs_db:
                job = jobs_db[job_id]
                job.status = JobStatus.FAILED
                job.error = str(e)
                jobs_db[job_id] = job

    def _safe_extract(self, results: List[Any], index: int) -> Dict[str, Any]:
        """
        Safely extract data from results list, handling exceptions.

        Args:
            results: List of results from data sources
            index: Index of the result to extract

        Returns:
            Extracted data or error information
        """
        if index >= len(results):
            return {"error": "Result index out of range"}

        result = results[index]
        if isinstance(result, Exception):
            return {"error": str(result)}

        return result

    async def _generate_report_sections(self, raw_data: Dict[str, Any]) -> Report:
        """
        Generate report sections using the LLM processor.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Structured Report object with all sections
        """
        # Generate each section concurrently
        tasks = [
            self.llm_processor.generate_company_overview(raw_data),
            self.llm_processor.generate_product_business_model(raw_data),
            self.llm_processor.generate_market_analysis(raw_data),
            self.llm_processor.generate_competitive_landscape(raw_data),
            self.llm_processor.generate_financial_metrics(raw_data),
            self.llm_processor.generate_fundraising_history(raw_data),
            self.llm_processor.generate_team_stakeholders(raw_data)
        ]

        results = await asyncio.gather(*tasks)

        # Create the report object
        report = Report(
            company_overview=results[0],
            product_business_model=results[1],
            market_analysis=results[2],
            competitive_landscape=results[3],
            financial_metrics=results[4],
            fundraising_history=results[5],
            team_key_stakeholders=results[6]
        )

        return report
