from privacy.policy.models import CURRENT_BUSINESS_RECORD_POLICY

def test_policy_v12():
    assert CURRENT_BUSINESS_RECORD_POLICY.version == "1.2"
    assert CURRENT_BUSINESS_RECORD_POLICY.required is True
    assert "회의록" in CURRENT_BUSINESS_RECORD_POLICY.body
