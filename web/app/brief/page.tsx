"use client";

import { useState } from "react";
import { createJob } from "@/lib/api";

export default function BriefPage() {
  const [topic, setTopic] = useState("10시에는 미국 대통령 도널드 트럼프 연설이 있습니다.");
  const [bullets, setBullets] = useState(
    "해당 연설 내용에 따라 급격한 변동성이 있을 수 있습니다.\n업무 간 참고하시길 바랍니다!!"
  );
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  return (
    <div style={{ maxWidth: 980, margin: "0 auto" }}>
      <h2>Brief</h2>

      <div style={{ display: "grid", gap: 12, background: "#151515", padding: 16, borderRadius: 12 }}>
        <label>
          Topic
          <input
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            style={{
              width: "100%",
              padding: 10,
              marginTop: 6,
              background: "#0f0f0f",
              color: "#fff",
              border: "1px solid #333",
            }}
          />
        </label>

        <label>
          Bullets (줄바꿈 = 항목)
          <textarea
            value={bullets}
            onChange={(e) => setBullets(e.target.value)}
            rows={5}
            style={{
              width: "100%",
              padding: 10,
              marginTop: 6,
              background: "#0f0f0f",
              color: "#fff",
              border: "1px solid #333",
            }}
          />
        </label>

        <button
          disabled={loading}
          onClick={async () => {
            setLoading(true);
            try {
              const payload = {
                channel_id: "channel-a",
                template_id: "template-card3",
                topic,
                bullets: bullets
                  .split("\n")
                  .map((s) => s.trim())
                  .filter(Boolean),
                target_seconds: 45,
                language: "ko",
              };
              const res = await createJob(payload);
              setResult(res);
            } finally {
              setLoading(false);
            }
          }}
          style={{
            padding: 12,
            borderRadius: 10,
            background: "#3d85f7",
            color: "#fff",
            border: 0,
            fontWeight: 700,
          }}
        >
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 18, background: "#151515", padding: 16, borderRadius: 12 }}>
          <div>
            job_id: <b>{result.job_id}</b>
          </div>
          <div>
            status: <b>{result.status}</b>
          </div>
          {result.output_mp4 && (
            <div>
              output: <code>{result.output_mp4}</code>
            </div>
          )}
          <div style={{ marginTop: 10 }}>
            <a href={`/review/${result.job_id}`} style={{ color: "#8ab4ff" }}>
              Review로 이동
            </a>{" "}
            |{" "}
            <a href="/drafts" style={{ color: "#8ab4ff" }}>
              Drafts 보기
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
