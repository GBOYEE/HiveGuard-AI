import pytest
from hiveguard_ai.src.audit_code import severity_value, gate

def test_severity_value():
    assert severity_value("Critical") == 10
    assert severity_value("High") == 8
    assert severity_value("Medium") == 5
    assert severity_value("Low") == 1

def test_gate_passes_low():
    summary = {"severity_label": "Low", "aggregate_severity": 2.0, "findings": []}
    assert gate(summary) is True

def test_gate_fails_high_severity():
    summary = {"severity_label": "High", "aggregate_severity": 8.0, "findings": []}
    assert gate(summary) is False

def test_gate_fails_critical_findings():
    summary = {"severity_label": "Low", "aggregate_severity": 2.0, "findings": [{"type": "Critical"}]}
    assert gate(summary) is False