import json
import sys
import os
ENFORCE_POLICY = os.getenv("ENFORCE_POLICY", "true").lower() == "true"

FAIL_LEVELS = {"high", "critical"}

def main(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    counts = {"low": 0, "moderate": 0, "high": 0, "critical": 0}

    # npm v7+ format
    if isinstance(data.get("vulnerabilities"), dict):
        for _, info in data["vulnerabilities"].items():
            sev = (info.get("severity") or "").lower()
            if sev in counts:
                counts[sev] += 1

    # older npm format
    elif isinstance(data.get("advisories"), dict):
        for _, adv in data["advisories"].items():
            sev = (adv.get("severity") or "").lower()
            if sev in counts:
                counts[sev] += 1

    print(f"Audit severity counts: {counts}")

    if ENFORCE_POLICY  and (counts["high"] > 0 or counts["critical"] > 0):
        print("❌ Policy fail: HIGH/CRITICAL vulnerabilities detected.")
        return 1

    print("✅ METRICS:no policy enforced.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/risk_score.py audit.json")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))