from pathlib import Path
import json

def run_scout(filepath: Path) -> dict:
    """Mock scanner: if file exists, return empty findings; if not, return error."""
    if not filepath.exists():
        return {"error": "File not found", "findings": []}
    # Simple placeholder: read file and count lines; real integration would call w3-scout
    try:
        text = filepath.read_text(errors="ignore")
        # Very basic heuristics: detect reentrancy pattern
        findings = []
        if "call{value:" in text or "call.value" in text:
            findings.append({"type": "reentrancy", "severity": "high"})
        return {"findings": findings, "lines": len(text.splitlines())}
    except Exception as e:
        return {"error": str(e), "findings": []}

def gate(summary: dict) -> bool:
    """Return True if passes security gate (Low severity, score < 7)."""
    label = summary.get("severity_label", "Low")
    score = summary.get("aggregate_severity", 0.0)
    if label in ("Critical", "High") or score >= 7.0:
        return False
    return True