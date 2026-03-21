import pytest
from hiveguard_ai.src.audit_code import run_scout, gate

def test_run_scout_missing_file(tmp_path):
    # Should handle missing file gracefully
    result = run_scout(tmp_path / "nonexistent.sol")
    assert "findings" in result

def test_gate_passes_on_low_severity():
    summary = {"aggregate_severity": 3.0, "severity_label": "Low", "findings": []}
    assert gate(summary) is True

def test_gate_fails_on_high():
    summary = {"aggregate_severity": 7.5, "severity_label": "High", "findings": [{"type":"reentrancy"}]}
    assert gate(summary) is False