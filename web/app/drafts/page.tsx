"use client";

import { useEffect, useMemo, useState } from "react";
import { getJobs, sendFeedback } from "@/lib/api";

function Bar({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "140px 1fr 50px", gap: 10, alignItems: "center" }}>
      <div style={{ color: "#bbb" }}>{label}</div>
      <div style={{ height: 10, background: "#222", borderRadius: 99, overflow: "hidden" }}>
        <div style={{ width: `${value}%`, height: 10, background: "#32d583" }} />
      </div>
      <div style={{ textAlign: "right" }}>{value}</div>
    </div>
  );
}

export default function DraftsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [selected, setSelected] = useState<any | null>(null);
  const [comment, setComment] = useState("");
  const [saved, setSaved] = useState<any>(null);

  useEffect(() => {
    (async () => {
      const list = await getJobs();
      setJobs(list);
      setSelected(list?.[0] ?? null);
    })();
  }, []);

  const scores = useMemo(() => selected?.eval?.scores ?? null, [selected]);

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto" }}>
      <h2>Drafts</h2>

      <div style={{ display: "grid", gridTemplateColumns: "360px 1fr", gap: 16 }}>
        <div style={{ background: "#151515", padding: 16, borderRadius: 12 }}>
          <div style={{ fontWeight: 700, marginBottom: 10 }}>Jobs</div>
          <div style={{ display: "grid", gap: 8 }}>
            {jobs.map((j) => (
              <button
                key={j.job_id}
                onClick={() => {
                  setSelected(j);
                  setSaved(null);
                }}
                style={{
                  textAlign: "left",
                  padding: 10,
                  borderRadius: 10,
                  border: "1px solid #2a2a2a",
                  background: selected?.job_id === j.job_id ? "#1f2b45" : "#0f0f0f",
                  color: "#fff",
                  cursor: "pointer",
                }}
              >
                <div style={{ fontWeight: 700 }}>{j.job_id}</div>
                <div style={{ color: "#bbb", fontSize: 12 }}>{j.status}</div>
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gap: 16 }}>
          <div style={{ background: "#151515", padding: 16, borderRadius: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ fontWeight: 700 }}>Scores</div>
              {selected?.job_id && (
                <div style={{ display: "flex", gap: 10 }}>
                  <a href={`/review/${selected.job_id}`} style={{ color: "#8ab4ff" }}>
                    Review
                  </a>
                  <a href={`/export/${selected.job_id}`} style={{ color: "#8ab4ff" }}>
                    Export
                  </a>
                </div>
              )}
            </div>

            {!scores ? (
              <div style={{ color: "#bbb", marginTop: 10 }}>선택된 job이 없거나 eval이 없습니다.</div>
            ) : (
              <div style={{ marginTop: 12, display: "grid", gap: 10 }}>
                {Object.entries(scores).map(([k, v]) => (
                  <Bar key={k} label={k} value={v as number} />
                ))}
              </div>
            )}
          </div>

          <div style={{ background: "#151515", padding: 16, borderRadius: 12, display: "grid", gap: 10 }}>
            <div style={{ fontWeight: 700 }}>Feedback</div>
            <textarea
              placeholder="피드백 코멘트 (bad일 때 룰셋에 누적됩니다)"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={4}
              style={{ padding: 10, background: "#0f0f0f", color: "#fff", border: "1px solid #333" }}
            />
            <button
              disabled={!selected?.job_id}
              onClick={async () => {
                const res = await sendFeedback(selected.job_id, {
                  verdict: "bad",
                  issue_type: "script",
                  comment,
                });
                setSaved(res);
              }}
              style={{ padding: 12, borderRadius: 10, background: "#3d85f7", color: "#fff", border: 0, fontWeight: 700 }}
            >
              저장
            </button>
            {saved && <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(saved, null, 2)}</pre>}
          </div>
        </div>
      </div>
    </div>
  );
}
