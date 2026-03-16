# HiveGuard AI – Secure Code Generation with Multi‑Agent RLHF

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active Development](https://img.shields.io/badge/Status-Active_Development-blue.svg)](https://github.com/GBOYEE/hiveguard-ai)

**An end‑to‑end AI safety agent that generates, aligns, and audits code using a hive of specialized agents.**  

HiveGuard AI demonstrates how to combine secure code generation, RLHF‑based alignment, and automated vulnerability scanning into a single pipeline. It leverages three existing open‑source projects:

- [`xander-hive-framework`](https://github.com/GBOYEE/xander-hive-framework) – Multi‑agent orchestration
- [`alignlab`](https://github.com/GBOYEE/alignlab) – RLHF dataset toolkit for underserved domains
- [`web3-security-scout`](https://github.com/GBOYEE/web3-security-scout) – Smart contract vulnerability scanner

This project is **open source** and part of a cohesive portfolio tackling AI safety from multiple angles.

---

## The Problem

AI code generators (e.g., GitHub Copilot, ChatGPT) can produce insecure code. Traditional solutions treat security as an afterthought. We need **secure by design** generation: the AI should *prefer* safe patterns and avoid vulnerabilities from the start.

---

## Our Solution

HiveGuard AI implements a three‑stage pipeline:

1. **Generate** – A hive of agents collaboratively writes code based on a prompt (using `xander-hive-framework`).
2. **Align** – RLHF preferences from `alignlab` (SecureCode dataset) rank the outputs, favoring secure implementations.
3. **Audit** – `web3-security-scout` scans the top‑ranked output for known vulnerability patterns; if issues remain, the loop can iterate.

The result: code that is both helpful and secure, with an auditable trail.

---

## Repository Structure

```
hiveguard-ai/
├── README.md
├── LICENSE (MIT)
├── requirements.txt
├── src/
│   ├── generate_code.py      # Step 1: hive‑based code generation
│   ├── align_output.py       # Step 2: apply RLHF ranking
│   └── audit_code.py         # Step 3: security scan
├── data/
│   └── samples/
│       └── secure_prefs.jsonl   # sample from AlignLab
├── docs/
│   ├── architecture.md
│   └── usage_guide.md
├── .github/
│   ├── FUNDING.yml
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
├── tests/
│   └── test_pipeline.py
└── landing.html
```

---

## Quickstart

```bash
git clone https://github.com/GBOYEE/hiveguard-ai.git
cd hiveguard-ai
pip install -r requirements.txt
python src/generate_code.py --prompt "Write a secure Python function that withdraws ETH from a smart contract."
python src/align_output.py --prefs data/samples/secure_prefs.jsonl --candidates candidates.jsonl
python src/audit_code.py --code output.py
```

See `docs/usage_guide.md` for detailed instructions.

---

## How It Integrates

- **xander‑hive** – Provides the multi‑agent environment. `generate_code.py` connects to the `developer` and `hunter` agents to produce candidate snippets.
- **alignlab** – Supplies the preference pairs (`secure_prefs.jsonl`) used by `align_output.py` to score each candidate.
- **web3‑security‑scout** – Its detection patterns are used in `audit_code.py` to flag potential vulnerabilities.

Together they form a closed‑loop safety system.

---

## Why This Matters for AI Jobs

- **Mercor**: Looking for ML Engineers who can build real‑world AI systems. HiveGuard shows you can integrate RLHF, security, and multi‑agent workflows into a coherent product.
- **Mindrift**: Focuses on AI training and feedback data. This project demonstrates deep理解 of how preference data improves model outputs, especially for code security.
- **General AI safety roles**: End‑to‑end safety pipelines are highly valued. HiveGuard is a concise, open‑source example you can discuss in interviews.

---

## Roadmap

- [ ] Replace mock generation with live hive agent calls
- [ ] Add human review UI (Label Studio) for preference labeling
- [ ] Support additional languages (Solidity, Rust, Go)
- [ ] Extend to non‑code domains (e.g., factual accuracy for educational content)
- [ ] Publish case study: fine‑tuning a 7B model with the aligned dataset

---

## Contributing

We welcome contributions! See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`. Issues and PRs are open for new detectors, RLHF improvements, and documentation.

---

## License

MIT – see `LICENSE`.

---

## Contact

Built by [@GBOYEE](https://github.com/GBOYEE) as part of a suite of AI safety tools.  
Collaboration? Open an issue or reach out via Calendly (link on landing page).
