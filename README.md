# Evaluation

## Project Goal
This project implements a CI-based dependency security pipeline for a single Node.js application that:
1) installs dependencies deterministically (`npm ci`),
2) produces machine-readable security artifacts (`npm audit` JSON + SBOM),
3) enforces a vulnerability policy gate that blocks merges when risk is unacceptable.

## Baseline Repository Context (nodejs-goof)
The selected target repository (nodejs-goof) is an intentionally vulnerable Node.js application designed for security training. Its dependency set includes known vulnerable packages and transitive dependencies on purpose. This makes it a good test case to validate that a CI “security gate” is able to detect and prevent risky dependency states from being merged.

## Snapshot Table (Baseline vs Updates)
> Fill in “Update #1 / Update #2” after you merge Dependabot PRs (or manual upgrade PRs) and download the `audit.json` artifact from the **run on `main`**.

| Snapshot | Date (YYYY-MM-DD) | Source (Run/PR) | Low | Moderate | High | Critical | Gate Result | Notes |
|---------:|-------------------|-----------------|----:|---------:|-----:|---------:|------------|------|
| Baseline | 2026-03-06 | GitHub Actions (main) | 8 | 32 | 66 | 36 | **Fail** | Intentionally vulnerable repo; expected to fail policy |
| Update #1 | 2026-03-06 | PR | 8 | 32 | 66 | 36 | **Fail** |  dependency-security Failed Because the way risk_score Script is set. second run will allow high risks for testing auto merge purposes.  |
| Update #2 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | e.g., additional upgrades / policy tuning |

## Baseline Measurements (Before Any Dependency Updates)
Source: GitHub Actions run (dependency-security job), output from `scripts/risk_score.py` using `npm audit --json`.

- **Low:** 8  
- **Moderate:** 32  
- **High:** 66  
- **Critical:** 36  

Artifacts collected from the workflow run:
- `audit.json` (npm audit report)
- `sbom.json` (CycloneDX SBOM)

## Policy Gate Result
The dependency-security job fails intentionally when **HIGH** or **CRITICAL** vulnerabilities are present.

**Observed behavior:**  
The workflow prints the severity counts and then exits with failure because high/critical vulnerabilities exist. This is expected for nodejs-goof.

## Why “This repo is deliberately insecure; the gate correctly blocks it.”
This repository is deliberately insecure by design, so a correctly configured security pipeline should *not* silently pass it. The gate is functioning as a preventative control:

- **It detects known-risk dependency states** (high/critical vulnerabilities) from the installed dependency graph (including transitive packages).
- **It blocks merging** when the risk level exceeds policy thresholds, which mirrors real-world secure development practices where severe known vulnerabilities must be addressed before release.
- **It still produces audit artifacts** (audit + SBOM) so the security team can track exactly what is vulnerable, prioritize fixes, and measure improvement over time.

In other words, the “failure” is not a CI malfunction—it's the intended security outcome proving the control works.

## Next Evaluation Steps (After Updates)
1) Merge a dependency update (e.g., a Dependabot PR that changes `package-lock.json`).
2) Re-run the pipeline on `main` and record new severity counts.
3) Compare before/after metrics:
   - change in vulnerability counts by severity,
   - time-to-remediate (PR opened → merged),
   - CI breakage rate for update PRs (tests/audit failures),
   - percentage of updates auto-merged vs blocked by policy.

## Notes / Assumptions
- `npm ci` is deterministic and does not upgrade packages. Vulnerability counts will not change until dependency versions in `package-lock.json` change (via Dependabot or manual updates), or unless the underlying vulnerability database changes.