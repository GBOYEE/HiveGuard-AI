#!/usr/bin/env python3
"""
Simple RLHF alignment: score candidates against secure preferences.
"""
import json, argparse, sys
from pathlib import Path

def load_prefs(prefs_path):
    prefs = []
    with open(prefs_path) as f:
        for line in f:
            if line.strip():
                prefs.append(json.loads(line))
    return prefs

def score_candidate(code: str, prefs) -> float:
    score = 0.0
    code_low = code.lower()
    for pref in prefs:
        good = pref.get("good", "")
        bad = pref.get("bad", "")
        if good and good.lower() in code_low:
            score += 1.0
        if bad and bad.lower() in code_low:
            score -= 2.0
    return score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default="candidates.jsonl")
    parser.add_argument("--prefs", required=True)
    parser.add_argument("--out", default="aligned.jsonl")
    args = parser.parse_args()

    prefs = load_prefs(args.prefs)
    candidates = []
    with open(args.candidates) as f:
        for line in f:
            cand = json.loads(line)
            cand["alignment_score"] = score_candidate(cand["code"], prefs)
            candidates.append(cand)

    # Sort by score descending
    candidates.sort(key=lambda x: x["alignment_score"], reverse=True)
    out_path = Path(args.out)
    with out_path.open("w") as f:
        for cand in candidates:
            f.write(json.dumps(cand) + "\n")
    print(f"Aligned {len(candidates)} candidates → {out_path} (best score: {candidates[0]['alignment_score'] if candidates else 'N/A'})")

if __name__ == "__main__":
    main()