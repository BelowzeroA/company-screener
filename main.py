"""
Main FastAPI application entry point for the Company Screener service.
"""
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException

from dotenv import load_dotenv

load_dotenv()

from app.models.report import ReportModel
from app.schemas.request import ReportRequest
from app.schemas.response import JobResponse, ReportResponse
from app.processors.report_generator import ReportGenerator
from app.models.job import ScreenerJob, JobStatus, jobs_db

app = FastAPI(
    title="Company Screener API",
    description="API for generating structured company reports based on a URL",
    version="0.1.0",
)

@app.post("/generate", response_model=JobResponse)
async def generate(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Initiates the process of generating a company report based on a URL.
    Returns a job ID for tracking the report generation process.
    """
    job_id = str(uuid.uuid4())

    # Create and store the job
    job = ScreenerJob(id=job_id, status=JobStatus.PENDING, url=str(request.url))
    jobs_db[job_id] = job

    # Start the report generation in the background
    report_gen = ReportGenerator(job_id=job_id)
    background_tasks.add_task(
        report_gen.generate_report_async,
        url=str(request.url)
    )

    return JobResponse(job_id=job_id, status=JobStatus.PENDING)


@app.get("/job/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    """
    Check the status of a report generation job.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs_db[job_id]
    return JobResponse(job_id=job_id, status=job.status)


@app.get("/report/{job_id}", response_model=ReportModel)
async def get_report(job_id: str):
    """
    Retrieve the generated report if the job has completed.
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs_db[job_id]

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Report not yet ready. Current status: {job.status}"
        )

    return job.report


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "service": "Company Screener API",
        "version": "0.1.0",
        "endpoints": [
            "/generate",
            "/job/{job_id}",
            "/report/{job_id}",
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

