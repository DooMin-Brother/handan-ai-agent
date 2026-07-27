# 한단 산업자동화 AI Agent v0.1

MASTER_REQUIREMENTS v1.1 기반의 **Architecture / 실행 가능한 프로젝트 골격**입니다.

## 현재 목적

지금 버전은 완성 서비스가 아니라, 수만 줄 규모로 확장할 때도 기능을 교체·추가하기 쉬운
모듈 구조를 먼저 검증하기 위한 버전입니다.

## 설치

Python 3.11 이상 권장.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## Gemini API Key

`.env.example`을 참고하십시오.

Streamlit Cloud를 사용할 경우 Secret에:

```toml
GEMINI_API_KEY="..."
GEMINI_MODEL="gemini-3.6-flash"
```

를 설정할 수 있습니다.

로컬 환경에서는 환경변수로 설정합니다.

API Key가 없어도 앱은 개발용 Fallback 모드로 실행됩니다.

## 실행

```bash
streamlit run app.py
```

## 현재 실제 동작

- Streamlit Chat UI
- In-Memory 대화
- Custom Session Set 수동 입력
- Agent Controller → Planner → Tool Registry → AI Service 흐름
- Gemini API Key가 있으면 Gemini 사용
- API Key가 없으면 Fallback
- 회원등급 Retention Policy 계산 구조

## 아직 실제 연결되지 않은 기능

- Google Cloud Memory
- 실제 RAG
- 실제 Semantic Cache
- PDF/사진/동영상
- 음성
- 동적 Report 파일 출력
- 고객 회원/권한
- 관리자 분석

위 기능들은 `docs/DEVELOPMENT_PLAN.md` 순서대로 추가합니다.

## 기준 문서

- `docs/MASTER_REQUIREMENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/CHANGELOG.md`
