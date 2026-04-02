"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { finalMp4Url, getJob } from "@/lib/api";

export default function ExportPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<any>(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const j = await getJob(jobId);
        setJob(j);
      } catch (e: any) {
        setErr(String(e?.message ?? e));
      }
    })();
  }, [jobId]);

  const src = finalMp4Url(jobId);

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto" }}>
      <h2>Export: {jobId}</h2>

      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <a href={`/review/${jobId}`} style={{ color: "#8ab4ff" }}>
          Review
        </a>
        <a href="/drafts" style={{ color: "#8ab4ff" }}>
          Drafts
        </a>
      </div>

      {err && <div style={{ color: "#ff8b8b" }}>{err}</div>}

      <div style={{ background: "#151515", padding: 16, borderRadius: 12 }}>
        <div>status: <b>{job?.status ?? "..."}</b></div>
        <div style={{ marginTop: 10 }}>
          <video src={src} controls style={{ width: "100%", maxWidth: 720, borderRadius: 12, background: "#000" }} />
        </div>
        <div style={{ marginTop: 10 }}>
          <a href={src} style={{ color: "#8ab4ff" }}>
            final.mp4 다운로드
          </a>
        </div>
      </div>
    </div>
  );
}
