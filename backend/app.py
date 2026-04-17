import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from studio.schemas import BriefIn, JobOut, FeedbackIn
from studio.harness import run_job, submit_feedback
from studio.store import ensure_dirs, job_dir, read_json
from studio.config import OUTPUT_DIR

app = FastAPI(title="Shortsauto Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/jobs", response_model=JobOut)
async def create_job(brief: BriefIn):
    ensure_dirs()
    job = await run_job(brief.model_dump())
    return job


@app.get("/jobs")
def list_jobs():
    ensure_dirs()
    if not os.path.exists(OUTPUT_DIR):
        return []

    items = []
    for name in os.listdir(OUTPUT_DIR):
        d = os.path.join(OUTPUT_DIR, name)
        if not os.path.isdir(d):
            continue
        output_mp4 = os.path.join(d, "final.mp4")
        eval_path = os.path.join(d, "eval_final.json")
        eval_text_path = os.path.join(d, "eval_text.json")

        ev = read_json(eval_path, default=None)
        ev_text = read_json(eval_text_path, default=None)

        status = "UNKNOWN"
        if os.path.exists(output_mp4):
            status = "DONE"
        elif ev_text and ev_text.get("pass_fail") == "FAIL":
            status = "FAILED_TEXT_QA"
        elif ev_text and ev_text.get("pass_fail") == "PASS":
            status = "RENDERING"

        items.append(
            {
                "job_id": name,
                "status": status,
                "output_mp4": output_mp4 if os.path.exists(output_mp4) else None,
                "eval": ev or ev_text,
            }
        )

    items.sort(key=lambda x: x["job_id"], reverse=True)
    return items


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    d = job_dir(job_id)
    if not os.path.exists(d):
        raise HTTPException(status_code=404, detail="job not found")

    output_mp4 = os.path.join(d, "final.mp4")
    script = read_json(os.path.join(d, "script.json"), default=None)
    ev = read_json(os.path.join(d, "eval_final.json"), default=None)
    ev_text = read_json(os.path.join(d, "eval_text.json"), default=None)

    status = "UNKNOWN"
    if os.path.exists(output_mp4):
        status = "DONE"
    elif ev_text and ev_text.get("pass_fail") == "FAIL":
        status = "FAILED_TEXT_QA"
    elif ev_text and ev_text.get("pass_fail") == "PASS":
        status = "RENDERING"

    return {
        "job_id": job_id,
        "status": status,
        "output_mp4": output_mp4 if os.path.exists(output_mp4) else None,
        "script": script,
        "eval": ev or ev_text,
    }


@app.get("/jobs/{job_id}/script")
def get_job_script(job_id: str):
    d = job_dir(job_id)
    p = os.path.join(d, "script.json")
    if not os.path.exists(p):
        raise HTTPException(status_code=404, detail="script not found")
    return read_json(p)


@app.get("/jobs/{job_id}/eval")
def get_job_eval(job_id: str):
    d = job_dir(job_id)
    p = os.path.join(d, "eval_final.json")
    if os.path.exists(p):
        return read_json(p)
    p2 = os.path.join(d, "eval_text.json")
    if os.path.exists(p2):
        return read_json(p2)
    raise HTTPException(status_code=404, detail="eval not found")


@app.get("/jobs/{job_id}/file/final.mp4")
def download_final(job_id: str):
    d = job_dir(job_id)
    p = os.path.join(d, "final.mp4")
    if not os.path.exists(p):
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(p, media_type="video/mp4", filename="final.mp4")


@app.post("/jobs/{job_id}/feedback")
async def feedback(job_id: str, fb: FeedbackIn):
    return submit_feedback(job_id, fb.model_dump())
