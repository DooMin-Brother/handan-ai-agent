from dataclasses import dataclass

BUSINESS_RECORD_POLICY_TEXT = (
    "원활한 기술지원과 지속적인 서비스 개선을 위해 AI 질의응답, 작업기록, "
    "생성된 보고서·회의록 등의 업무기록은 회원등급에 따른 기간 동안 저장되며, "
    "보존기간이 지나면 관련 기록은 정책에 따라 삭제됩니다. 필요한 경우 원활한 "
    "기술지원 및 고객지원을 위한 자료로 활용될 수 있습니다."
)

@dataclass(frozen=True)
class PolicyVersion:
    policy_type: str
    version: str
    title: str
    body: str
    required: bool = True

CURRENT_BUSINESS_RECORD_POLICY = PolicyVersion(
    policy_type="business_record_management",
    version="1.2",
    title="AI 기술지원 서비스 이용 및 업무기록 관리",
    body=BUSINESS_RECORD_POLICY_TEXT,
)
