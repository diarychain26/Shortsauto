# Shortsauto (Shorts Studio Clone MVP)

자동 쇼츠 생산 파이프라인 MVP입니다.

- Script 자동 생성 (채널/템플릿/룰 기반)
- 이미지 자동 생성 (Google Gemini Nano Banana / Nano Banana Pro 지원)
- 음성 자동 생성 (TTS Provider: Edge 기본 / Typecast 플러그인)
- ffmpeg 렌더 → 최종 mp4
- Evaluator 점수 + PASS/FAIL
- 사람 피드백 → 룰 업데이트(상태 유지)

## 구조

- `backend/` FastAPI + 렌더 파이프라인
- `web/` Next.js UI (Brief / Drafts / Review / Export)

## Backend 실행

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

# ffmpeg 설치 필요
uvicorn app:app --reload
```

### 생성 요청 예시

```bash
curl -X POST "http://127.0.0.1:8000/jobs" \
  -H "Content-Type: application/json" \
  -d "{\"channel_id\":\"channel-a\",\"template_id\":\"template-card3\",\"topic\":\"10시에는 미국 대통령 도널드 트럼프 연설이 있습니다.\",\"bullets\":[\"해당 연설 내용에 따라 급격한 변동성이 있을 수 있습니다.\",\"업무 간 참고하시길 바랍니다!!\"],\"target_seconds\":45,\"language\":\"ko\"}"
```

결과 mp4: `backend/storage/outputs/<job_id>/final.mp4`

### 조회 API

- `GET /jobs` (job 목록)
- `GET /jobs/{job_id}` (job 상세)
- `GET /jobs/{job_id}/script`
- `GET /jobs/{job_id}/eval`
- `GET /jobs/{job_id}/file/final.mp4` (다운로드/재생)

## Web UI 실행

```bash
cd web
npm i
# .env.local 만들기 (예: NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000)
npm run dev
```

브라우저: `http://localhost:3000/brief`

## 이미지 생성: Gemini Nano Banana2(요청 반영)

사용자가 말한 "나노바나나2"는 앱/마케팅 명칭에 가깝고, Gemini API에서는 이미지 모델이 아래처럼 노출됩니다.

- 기본(빠름): `gemini-2.5-flash-image`
- 고품질(텍스트/복잡 지시): `gemini-3-pro-image-preview`

### 설정

`backend/.env`에서:

```bash
IMAGE_PROVIDER=gemini
GEMINI_API_KEY=YOUR_KEY
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
```

## Typecast TTS 연동

`backend/studio/tts/typecast_provider.py`의 endpoint/필드명을 Typecast 문서에 맞게 수정.

- `backend/.env` 또는 환경변수:
  - `TTS_PROVIDER=typecast`
  - `TYPECAST_API_KEY=...`
  - `TYPECAST_VOICE_ID=...`
