"""
Backend API for FailProof LLM.

This module defines the FastAPI application and its endpoints for the read-only API.
It provides endpoints to retrieve information about test runs, test cases, and
generated reports.
"""
from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from ...backend.storage import models, database
from ...backend.core.contracts import Run, SuiteStats, RunResult

app = FastAPI()

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.detail}},
    )

@app.on_event("startup")
async def startup_event():
    """
    Generate the OpenAPI schema and save it to a file.
    """
    openapi_schema = app.openapi()
    with open("backend/api/openapi.json", "w") as f:
        json.dump(openapi_schema, f)

# API Key Authentication
API_KEY = os.getenv("API_KEY")

async def api_key_auth(x_api_key: str = Header(None)):
    if not API_KEY:
        # If no API_KEY is set in the environment, disable auth
        return
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Dependency to get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthz")
def health_check():
    return {"status": "ok", "version": "0.1.0", "commit": "TBD"}

api_v1 = FastAPI(dependencies=[Depends(api_key_auth)])

@api_v1.get("/runs", response_model=List[Run])
def get_runs(db: Session = Depends(get_db), limit: int = 50, cursor: Optional[str] = None):
    """
    Retrieve a list of all test runs.
    """
    query = db.query(models.RunResultDB).distinct(models.RunResultDB.run_id)
    if cursor:
        query = query.filter(models.RunResultDB.run_id > cursor)
    runs = query.limit(limit).all()
    
    results = []
    for run in runs:
        total_cases = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == run.run_id).count()
        pass_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == run.run_id, models.RunResultDB.classification['primary'] == 'pass').count()
        fail_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == run.run_id, models.RunResultDB.classification['primary'] == 'fail').count()
        error_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == run.run_id, models.RunResultDB.error != None).count()

        suite_stats = SuiteStats(
            suite_id=run.suite_id,
            total_cases=total_cases,
            pass_count=pass_count,
            fail_count=fail_count,
            error_count=error_count,
        )
        
        results.append(Run(
            run_id=run.run_id,
            model_id=run.model_id,
            timestamp_utc=run.timestamp_utc.isoformat(),
            suite_stats=suite_stats
        ))
    return results

@api_v1.get("/runs/{id}", response_model=Run)
def get_run(id: str, db: Session = Depends(get_db)):
    """
    Retrieve detailed information for a single test run.
    """
    run = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    total_cases = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id).count()
    pass_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id, models.RunResultDB.classification['primary'] == 'pass').count()
    fail_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id, models.RunResultDB.classification['primary'] == 'fail').count()
    error_count = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id, models.RunResultDB.error != None).count()

    suite_stats = SuiteStats(
        suite_id=run.suite_id,
        total_cases=total_cases,
        pass_count=pass_count,
        fail_count=fail_count,
        error_count=error_count,
    )
    
    return Run(
        run_id=run.run_id,
        model_id=run.model_id,
        timestamp_utc=run.timestamp_utc.isoformat(),
        suite_stats=suite_stats
    )

@api_v1.get("/runs/{id}/cases", response_model=List[RunResult])
def get_run_cases(id: str, db: Session = Depends(get_db), limit: int = 50, cursor: Optional[str] = None):
    """
    Retrieve all test case results for a specific run.
    """
    query = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id)
    if cursor:
        query = query.filter(models.RunResultDB.case_id > cursor)
    cases = query.limit(limit).all()
    if not cases:
        raise HTTPException(status_code=404, detail="Cases not found for this run")
    return cases

@api_v1.get("/cases/{id}", response_model=RunResult)
def get_case(id: str, db: Session = Depends(get_db)):
    """
    Retrieve detailed information for a single test case result.
    """
    case = db.query(models.RunResultDB).filter(models.RunResultDB.case_id == id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@api_v1.get("/runs/{id}/report.md")
def get_run_report(id: str, db: Session = Depends(get_db)):
    """
    Retrieve the full Markdown report for a specific run.
    """
    run = db.query(models.RunResultDB).filter(models.RunResultDB.run_id == id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # This is a placeholder for the actual report generation logic.
    # In a real implementation, this would generate a Markdown report
    # based on the run data.
    report_content = f"# Test Run Report: {id}\\n\\nThis is a sample report."
    return report_content

app.mount("/api/v1", api_v1)