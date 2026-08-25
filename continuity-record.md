# Continuity Record — UBI Stage 8

## 1. Prior-Stage Component Reused

- **Previous Stage**: Stage 7 (IAM Chain)
- **Previous Stage Commit**: `6d5559c`
- **Components reused as patterns**:
  - Evidence index format (claim_id, artifact, locator, proves/doesn't prove)
  - JSONL event logging (provided by portable_range.py)
  - Before/after graph diff for remediation proof
  - Cleanup verification model (temporary objects = 0)

## 2. Interface Consumed

- Same evidence-index.csv format from Stage 7
- Same JSONL event sequence pattern
- Same remediation assertion pattern

## 3. Migration Record

| Stage 7 (AWS IAM) | Stage 8 (AD Directory) | Reason |
|---|---|---|
| AWSIdentityRegistry | Dynamic SID resolution | Cloud → on-prem identity |
| CloudTrail events | portable_range.py events | Cloud audit → local event ledger |
| IAM policy remediation | ACL/SPN remediation | Cloud permissions → directory permissions |

## 4. Hand-off to Stage 9

- Graph schema with versioned edges
- Edge validation with raw source records
- Detection rules with positive/benign fixtures
- Remediation with graph diff proof
