from __future__ import annotations
import asyncio
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field
from config import settings
from orchestrator import SwarmResult, run_swarm


app = FastAPI(title="IntelSwarm API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    company: str = Field(..., min_length=1, max_length=100)


@dataclass
class JobState:
    queue: asyncio.Queue[str] = field(default_factory=asyncio.Queue)
    result: SwarmResult | None = None


jobs: dict[str, JobState] = {}


async def publish(job_id: str, payload: dict[str, object]) -> None:
    job = jobs[job_id]
    await job.queue.put(f"data: {json.dumps(payload)}\n\n")


async def run_job(job_id: str, company: str) -> None:
    try:
        result = await run_swarm(company, progress_callback=lambda event: publish(job_id, event))
        jobs[job_id].result = result
        await publish(
            job_id,
            {
                "status": "done",
                "report": result.markdown,
                "report_path": result.report_path.name,
                "scores": result.section_scores,
            },
        )
    except Exception as exc:  # pragma: no cover - surfaced to client stream
        await publish(job_id, {"status": "error", "message": str(exc)})
    finally:
        await jobs[job_id].queue.put("event: close\ndata: {}\n\n")


@app.post("/research")
async def start_research(payload: ResearchRequest, background_tasks: BackgroundTasks) -> dict[str, str]:
    company = payload.company.strip()
    if not company:
        raise HTTPException(status_code=400, detail="Company name is required.")

    job_id = str(uuid.uuid4())
    jobs[job_id] = JobState()
    background_tasks.add_task(run_job, job_id, company)
    return {"job_id": job_id}


@app.get("/research/{job_id}/stream")
async def stream_research(job_id: str) -> StreamingResponse:
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Research job not found.")

    async def event_generator():
        queue = jobs[job_id].queue
        try:
            while True:
                message = await queue.get()
                yield message
                if message.startswith("event: close"):
                    break
        finally:
            jobs.pop(job_id, None)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/reports")
async def list_reports() -> dict[str, list[dict[str, str]]]:
    reports = []
    for path in sorted(settings.reports_dir.glob("*.md"), reverse=True):
        stem = path.stem
        parts = stem.rsplit("_", 2)
        if len(parts) == 3:
            company = parts[0]
            timestamp = f"{parts[1]}_{parts[2]}"
        else:
            company, timestamp = stem, ""
        reports.append(
            {
                "company": company.replace("_", " ").title(),
                "timestamp": timestamp,
                "filename": path.name,
            }
        )
    return {"reports": reports}


@app.get("/reports/{filename}")
async def get_report(filename: str) -> PlainTextResponse:
    path = (settings.reports_dir / filename).resolve()
    if settings.reports_dir.resolve() not in path.parents or not path.exists():
        raise HTTPException(status_code=404, detail="Report not found.")
    return PlainTextResponse(path.read_text(encoding="utf-8"))
