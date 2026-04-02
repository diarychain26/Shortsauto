"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getScript } from "@/lib/api";

export default function ReviewPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [script, setScript] = useState<any>(null);
  const [err, setErr] = useState<string>("");

  useEffect(() => {
    (async () => {
      try {
        const s = await getScript(jobId);
        setScript(s);
      } catch (e: any) {
        setErr(String(e?.message ?? e));
      }
    })();
  }, [jobId]);

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto" }}>
      <h2>Review: {jobId}</h2>

      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <a href={`/export/${jobId}`} style={{ color: "#8ab4ff" }}>
          Export
        </a>
        <a href="/drafts" style={{ color: "#8ab4ff" }}>
          Drafts
        </a>
      </div>

      {err && <div style={{ color: "#ff8b8b" }}>{err}</div>}

      {!script ? (
        <div style={{ color: "#bbb" }}>Loading...</div>
      ) : (
        <div style={{ display: "grid", gap: 12 }}>
          <div style={{ background: "#151515", padding: 16, borderRadius: 12 }}>
            <div style={{ fontWeight: 700, marginBottom: 8 }}>Full Text</div>
            <pre style={{ whiteSpace: "pre-wrap" }}>{script.full_text}</pre>
          </div>

          {script.scenes?.map((s: any) => (
            <div key={s.idx} style={{ background: "#151515", padding: 16, borderRadius: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <div style={{ fontWeight: 700 }}>Scene {s.idx}</div>
                <div style={{ color: "#bbb" }}>{s.duration_sec}s</div>
              </div>
              <div style={{ marginTop: 10, display: "grid", gap: 6 }}>
                <div style={{ color: "#bbb" }}>On-screen text</div>
                <ul>
                  {s.on_screen_text?.map((t: string, i: number) => (
                    <li key={i}>{t}</li>
                  ))}
                </ul>
                <div style={{ color: "#bbb" }}>Narration</div>
                <div>{s.narration}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
