# Security Gate

## Purpose

To ensure that generated code meets a minimum security standard before being presented as final output, HiveGuard AI integrates `web3-security-scout` as an automated audit step. The gate rejects code with High or Critical severity findings.

## How It Works

1. After alignment, the top candidate code is written to a temporary file (e.g., `output.sol`).
2. The `audit_code.py` script runs:
   ```bash
   w3-scout output.sol --json
   ```
3. It computes the aggregate severity (CVSS 0–10) and checks the severity label.
4. If any finding has severity ≥ 7 (High) or the aggregate label is High/Critical, the gate fails.
5. Upon failure, the pipeline can loop back to generate new candidates or alert a human reviewer.

## CLI Usage

```bash
python src/audit_code.py --code output.sol --report security_report.json
```

Exit codes:
- 0: passed
- 1: failed security gate
- 2: scanner error

## Integration Example

In a full pipeline:
```bash
python src/generate_code.py --prompt "Write a safe ERC20 token" --out candidates.jsonl
python src/align_output.py --candidates candidates.jsonl --prefs data/samples/secure_prefs.jsonl --out aligned.jsonl
# take top candidate
jq -r '.code' aligned.jsonl > output.sol
python src/audit_code.py --code output.sol
if [ $? -eq 0 ]; then
  echo "Approved"
else
  echo "Rejected; need improvement"
fi
```

## Customization

Adjust the severity threshold by editing `severity_value()` in `audit_code.py`. For stricter gating, reject Medium as well (`score >= 4`).