# Shortsauto (Shorts Studio Clone MVP)

자동 쇼츠 생산 파이프라인 MVP입니다.

- Script 자동 생성 (채널/템플릿/룰 기반)
- 이미지 자동 생성(카드뉴스 템플릿)
- 음성 자동 생성(TTS Provider: Edge 기본 / Typecast 플러그인)
- ffmpeg 렌더 → 최종 mp4
- Evaluator 점수 + PASS/FAIL
- 사람 피드백 → 룰 업데이트(상태 유지)

## 빠른 실행 (Backend)

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt

# ffmpeg 설치 필요
uvicorn app:app --reload
```

생성 요청 예시:
```bash
curl -X POST "http://127.0.0.1:8000/jobs" \
  -H "Content-Type: application/json" \
  -d "{\"channel_id\":\"channel-a\",\"template_id\":\"template-card3\",\"topic\":\"10시에는 미국 대통령 도널드 트럼프 연설이 있습니다.\",\"bullets\":[\"해당 연설 내용에 따라 급격한 변동성이 있을 수 있습니다.\",\"업무 간 참고하시길 바랍니다!!\"],\"target_seconds\":45,\"language\":\"ko\"}"
```

결과 mp4는 `backend/storage/outputs/<job_id>/final.mp4`

## Web UI (Next.js)

```bash
cd web
npm i
npm run dev
```

브라우저에서 `http://localhost:3000/brief`

> Web은 MVP용 UI 골격입니다. Backend에 목록/스크립트 조회 API를 추가하면 Drafts/Review가 완전히 동작합니다.

## Typecast TTS 연동

`backend/studio/tts/typecast_provider.py` 에 Typecast API 스펙에 맞게 엔드포인트/페이로드만 수정하세요.
`.env`에서 `TTS_PROVIDER=typecast` 설정.
