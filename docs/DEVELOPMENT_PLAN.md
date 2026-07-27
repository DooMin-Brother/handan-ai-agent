# Development Plan

## Phase 0 — Architecture / Skeleton [현재]
- [x] MASTER_REQUIREMENTS v1.1 반영
- [x] 모듈 구조
- [x] Agent/Tool/Repository Interface
- [x] Streamlit 기본 실행
- [x] Gemini Adapter
- [x] In-Memory 개발 Repository
- [x] Custom Session Set 기본 구조
- [x] RAG/Semantic Cache 경계
- [x] Retention Policy 경계
- [x] 테스트 기본 구조

## Phase 1 — 대화/세션 기반
- Gemini 대화 Context 개선
- 세션 생성/종료/목록/복원
- 사용자/고객 기본 도메인
- Custom Session Set UI 개선
- 파일 업로드 경계 추가
- 대화/세션 데이터 모델 확정

## Phase 2 — Google Cloud Memory
- Google Cloud 프로젝트 연결
- Repository Adapter 구현
- 세션/대화/회원등급 저장
- Cloud Storage 첨부파일 저장
- Retention metadata
- 개발/운영 환경 분리
- 권한 및 Secret 관리

## Phase 3 — Manual Ingestion / RAG
- 매뉴얼 Cloud upload
- 문서 Metadata 자동 추출
- Chunking
- Embedding
- Vector Index
- Session Set 우선 Retriever
- Citation/페이지 근거
- 전체 DB 확장 검색

## Phase 4 — Semantic Cache
- embedding 기반 의미 유사도
- 제조사/모델/버전/Session Context 검증
- TTL / invalidation
- 비용/Cache hit 분석

## Phase 5 — Multimodal / Agent Tools
- PDF/문서
- 이미지/화면 캡처
- 동영상
- 음성 질의
- Tool plugin 확장
- Agent Planning 고도화

## Phase 6 — Dynamic Reports
- 작업목적 자동 판단
- 문서 구조 자동 생성
- 고객/사내/경영진 Context
- DOCX/PDF Export
- 만료 전 결과문서 안내

## Phase 7 — Customer / Retention
- 회원등급
- 권한
- 등급별 보존기간
- 만료 알림
- 자동 삭제
- 중요 세션 연장
- 지식화 승인/비식별 정책

## Phase 8 — Admin Analytics
- AI 경영 요약
- 사용현황
- 기술수요 분석
- Business Insight
- 기술지원/교육/제품 Opportunity
- 영업 신호
- 사실/AI분석/추천 분리

## Phase 9 — Knowledge Base / 고도화
- 검증 해결사례
- 유사사례 검색
- 피드백
- 성능/비용 최적화
- 모델 라우팅
- 운영 모니터링

## 단계 진행 규칙

한 Phase를 완료할 때마다:
1. 테스트 통과
2. 기존 기능 회귀검증
3. CHANGELOG 작성
4. Git tag/버전 저장
5. 다음 Phase 진입

## v0.2 보강 — Privacy / Access Control
- [x] MASTER_REQUIREMENTS v1.2 반영
- [x] 업무기록 필수 안내 문구 코드화
- [x] Policy Version / Consent Record 구조
- [x] Access Control 경계
- [x] Audit Log 경계
- [x] 회의 음성 원본을 일반 업무기록과 분리
- [ ] 실제 회원가입 UI 연결
- [ ] 고객/조직 Role DB 연결
- [ ] Google Cloud Audit 저장
- [ ] 개인정보 처리방침 화면
