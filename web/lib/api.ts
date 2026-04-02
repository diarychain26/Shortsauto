const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

async function j<T>(r: Response): Promise<T> {
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createJob(payload: any) {
  return j(
    await fetch(`${API_BASE}/jobs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
}

export async function getJobs() {
  return j(await fetch(`${API_BASE}/jobs`));
}

export async function getJob(jobId: string) {
  return j(await fetch(`${API_BASE}/jobs/${jobId}`));
}

export async function getScript(jobId: string) {
  return j(await fetch(`${API_BASE}/jobs/${jobId}/script`));
}

export async function getEval(jobId: string) {
  return j(await fetch(`${API_BASE}/jobs/${jobId}/eval`));
}

export async function sendFeedback(jobId: string, payload: any) {
  return j(
    await fetch(`${API_BASE}/jobs/${jobId}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
}

export function finalMp4Url(jobId: string) {
  return `${API_BASE}/jobs/${jobId}/file/final.mp4`;
}
