## Security Automation Results (npm audit)

This repo is used to demonstrate an automated dependency security workflow for a single Node.js application:
- Deterministic installs with `npm ci`
- Vulnerability reporting with `npm audit --json`
- SBOM generation (CycloneDX)
- (Optional) Policy gate to block merges when HIGH/CRITICAL findings exist
- (Optional) Auto-merge for Dependabot PRs when checks pass

### Before vs After (audit snapshots)

These numbers come from the `npm audit --json` metadata produced by the CI workflow.

| Snapshot | Low | Moderate | High | Critical | Total |
|---|---:|---:|---:|---:|---:|
| Baseline (before updates) | 8 | 32 | 66 | 36 | 142 |
| After Update Cycle #1 | 0 | 8 | 16 | 14 | 38 |

**Change summary**
- Total vulnerabilities reduced by **104** (142 → 38), a **~73% reduction**
- Low: 8 → 0  
- Moderate: 32 → 8  
- High: 66 → 16  
- Critical: 36 → 14  

> Note: nodejs-goof is intentionally vulnerable for training purposes, so even after updates it is expected to still contain HIGH/CRITICAL findings. The security gate is meant to detect this and (in strict mode) block merges until risk is reduced.

### Dependency footprint (metadata)
| Snapshot | Prod deps | Dev deps | Optional deps | Total deps |
|---|---:|---:|---:|---:|
| Baseline (before updates) | 690 | 563 | 24 | 1274 |
| After Update Cycle #1 | 676 | 193 | 11 | 879 |

### Where to find the updated reports (Artifacts)
Each GitHub Actions run uploads:
- `audit.json` (the full npm audit report)
- `sbom.json` (CycloneDX SBOM)

To download them:
1. GitHub repo → **Actions**
2. Click the latest workflow run
3. Scroll to **Artifacts** → download `security-artifacts`

### Policy Gate (strict vs demo mode)
- **Strict mode (recommended for real projects):** fail the workflow if HIGH/CRITICAL vulnerabilities are present.
- **Demo / metrics-only mode:** still generate and upload the artifacts, but do not fail the job (useful for showing auto-merge behavior while still tracking risk).
