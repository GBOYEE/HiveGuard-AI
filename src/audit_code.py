#!/usr/bin/env python3
"""
Security audit and gating for generated code.
Uses web3-security-scout to detect vulnerabilities.
Fails (exit 1) if any finding has severity >= 7 (High/Critical).
"""
import sys, argparse, json, subprocess
from pathlib import Path

def run_scout(target_path: Path) -> dict:
    """Invoke w3-scout CLI and parse JSON output."""
    try:
        result = subprocess.run(
            ["w3-scout", str(target_path), "--json"],
            capture_output=True, text=True, check=False, timeout=60
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Scout error: {e}")
        sys.exit(2)

def severity_value(label: str) -> int:
    if label == "Critical": return 10
    if label == "High": return 8
    if label == "Medium": return 5
    return 1

def gate(summary: dict) -> bool:
    """Return True if passes security gate."""
    label = summary.get("severity_label", "Low")
    score = summary.get("aggregate_severity", 0.0)
    # Reject if any high/critical findings exist OR aggregate >= 7
    critical_findings = any(severity_value(f.get("type", "Low")) >= 9 for f in summary.get("findings", []))
    high_findings = any(severity_value(f.get("type", "Low")) >= 7 for f in summary.get("findings", []))
    if label in ("Critical", "High") or score >= 7.0 or critical_findings or high_findings:
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", required=True, help="Path to candidate code (solidity file)")
    parser.add_argument("--report", default="security_report.json", help="Where to save scout report")
    args = parser.parse_args()

    code_path = Path(args.code)
    if not code_path.exists():
        print(f"Code file not found: {code_path}")
        sys.exit(1)

    print(f"Scanning {code_path} with w3-scout...")
    summary = run_scout(code_path)
    # Save raw report
    with open(args.report, "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary to console
    print(f"Findings: {summary['total_findings']} | Severity: {summary.get('aggregate_severity')} ({summary.get('severity_label')})")

    if not gate(summary):
        print("Security gate FAILED. Code must be revised.")
        # Suggest actions
        print("Recommendations:")
        print("- Fix High/Critical vulnerabilities")
        print("- Re-run alignment and audit")
        sys.exit(1)
    else:
        print("Security gate PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()