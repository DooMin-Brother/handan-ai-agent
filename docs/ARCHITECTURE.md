# 한단 산업자동화 AI Agent — Architecture v0.2

## 1. 목적

MASTER_REQUIREMENTS v1.1을 실제 코드 구조로 옮기기 위한 기준 문서다.

목표는 코드가 수만 줄로 성장해도 특정 기능 변경이 다른 영역에 미치는 영향을
최소화하는 것이다.

## 2. 핵심 설계 원칙

### 2.1 Dependency Inversion
Agent는 Gemini, Google Cloud, 특정 Vector DB를 직접 호출하지 않는다.
항상 Interface → Service/Repository → Adapter 순서로 연결한다.

### 2.2 Open Tool Architecture
업무 종류를 고정하지 않는다.
새로운 능력은 Agent Tool을 추가하고 Tool Registry에 등록하는 방식으로 확장한다.

### 2.3 Data-driven Manufacturer Support
제조사별 Python 로직을 만들지 않는다.
제조사/제품/모델/문서종류/버전은 Metadata와 데이터로 관리한다.

### 2.4 UI Independence
Streamlit은 초기 UI일 뿐이다.
향후 React로 교체해도 Agent/Knowledge/Memory/Analytics는 재사용한다.

### 2.5 Cloud Independence inside Application Core
Google Cloud를 기본 인프라로 사용하되, 핵심 도메인 코드는 Google SDK에 직접 종속되지 않는다.

## 3. 주요 계층

```text
UI
 ↓
Agent Controller
 ↓
Planner / Context / Tool Registry
 ↓
Domain Services
 ├─ Memory
 ├─ Session Set
 ├─ RAG
 ├─ Semantic Cache
 ├─ Reports
 ├─ Retention
 └─ Analytics
 ↓
Repositories / Provider Interfaces
 ↓
Adapters
 ├─ Gemini
 └─ Google Cloud
```

## 4. Memory

Memory는 세 종류로 구분한다.

- Short-term: 현재 대화/현재 작업
- Long-term: 고객/프로젝트/세션 복원
- Organizational: 정책상 허용된 비식별 해결지식

원본 고객대화와 조직지식을 같은 저장 정책으로 취급하지 않는다.

## 5. Custom Session Set

한 세션에서 여러 브랜드/기종을 선택한다.

검색 우선순위:

1. Custom Session Set
2. 연관 제품/시스템
3. 전체 매뉴얼 DB

Session Set은 검색 제한이 아니라 우선순위다.

## 6. RAG + Semantic Cache

목표 흐름:

```text
질문
 ↓
Semantic Cache 후보 검색
 ↓
Context/기종/버전/Session 검증
 ↓ miss
RAG
 ↓
Session Set 우선 검색
 ↓ 부족 시 전체 검색
 ↓
Gemini
 ↓
근거/추론 분리 답변
 ↓
검증 가능한 결과 Cache 저장
```

v0.1의 Semantic Cache는 인터페이스/수명주기만 존재하며
실제 의미기반 캐시는 후속 단계에서 구현한다.

## 7. Retention

회원등급별로 원대화/첨부/영상 보존기간을 다르게 한다.

Retention은 다음 기능으로 독립된다.

- policy
- membership rules
- expiration
- notification
- anonymization
- deletion

만료 전 결과문서 제공과 알림을 지원하고,
고객 영업비밀 가능 자료를 자동 공용 지식화하지 않는다.

## 8. 관리자

확정된 관리자 구조:

- AI 경영 요약
- ① 사용현황
- ② 기술수요 분석
- ③ Business Insight

분석 결과는 항상 다음을 구분한다.

1. 확인된 데이터
2. AI 분석
3. 추천 행동

## 9. 동적 문서

문서 종류를 고정하지 않는다.

Agent가 다음 세 요소를 바탕으로 문서 구조를 결정한다.

- 작업 목적
- 전체 대화/작업 내용
- 사용자 최종 지시

생성된 논리 문서 모델과 PDF/DOCX Exporter를 분리한다.

## 10. 프로젝트 디렉터리

```text
app.py
agent/
analytics/
core/
customers/
docs/
integrations/
knowledge/
knowledge_base/
memory/
reports/
repositories/
retention/
services/
sessions/
tests/
tools/
ui/
```

## 11. v0.1에서 의도적으로 구현하지 않는 것

- Google Cloud 실제 리소스 생성
- 특정 Vector DB 확정
- 실제 RAG indexing
- 실제 embedding Semantic Cache
- 음성 입력
- 사진/동영상 처리
- 로그인/회원결제
- 관리자 분석 계산
- PDF/DOCX Export

이 기능들은 현재 골격의 Interface를 깨지 않고 단계적으로 추가한다.

## 12. 변경 규칙

새 기능 추가 전:
1. MASTER_REQUIREMENTS 확인
2. 영향 모듈 확인
3. Interface 변경 필요 여부 검토
4. 구현
5. 회귀 테스트
6. CHANGELOG 기록

확정 요구사항 삭제/축약/구조변경은 사용자 확인 없이 하지 않는다.



## 13. Privacy / Access Control

업무기록 저장과 관리자 접근을 핵심 Agent 로직과 분리한다.

```text
UI / Admin
    ↓
Access Control Service
    ↓
Permission Policy
    ↓
Business Record Repository
    ↓
Storage Adapter
```

관리자 분석은 집계/AI 분석을 우선 제공하고,
추가 기술지원이 필요한 경우에만 권한 있는 담당자가 원 업무기록에 접근한다.
원 업무기록 접근 시 Audit Log를 남길 수 있도록 한다.

## 14. Policy Versioning

회원이 어떤 버전의 필수 정책에 동의했는지 저장한다.

```text
user_id
policy_type
policy_version
status
agreed_at
withdrawn_at
```

## 15. Business Record Scope

- conversation
- work_session
- generated_report
- generated_minutes
- support_result
- attachment_processing_history

회의 음성 원본은 별도 데이터 범주로 관리한다.

## 16. Retention + Access Control

```text
업무기록 생성
   ↓
회원등급별 Retention Policy
   ↓
저장
   ↓
권한 기반 접근
   ↓
필요 시 Audit Log
   ↓
만료 전 안내
   ↓
기간 만료
   ↓
정책에 따른 원본 삭제
```
