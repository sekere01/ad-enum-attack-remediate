# Stage 8: Break and Repair the Directory Control Plane

## Variant: D5 | Marker: UBI-A8-E7C1EEB30702

## Quick Start

```bash
# 1. Verify archive and candidate JSON
sha256sum ethical-hacking-stage-8-shared-b2.tar.gz
python3 evidence/lab-source/portable_range.py verify \
  --assignment candidate.json --hash 9a9d9c3fcf301ed7fc069e75a1485037071b84978d7f61052fefcf48f5ab17b5

# 2. Provision range (test surface)
python3 evidence/lab-source/portable_range.py provision \
  --assignment candidate.json --out range

# 3. Build full graph (7 nodes, 9 edges)
python3 -m src.graph_builder --root range --out output/enumeration

# 4. Validate edges (8 valid, 1 rejected)
python3 -m src.edge_validator --graph output/enumeration/graph.json \
  --root range --out output/enumeration

# 5. Find attack paths
python3 -m src.path_finder --graph output/enumeration/graph.json \
  --root range --out output/attack-paths.json

# 6. Run automation (3 clean runs from fresh state)
python3 -m src.automation --assignment candidate.json --root range

# 7. Run detections
python3 -m src.detections --root range --out output/detections

# 8. Apply remediations
python3 -m src.remediation --assignment candidate.json --root range

# 9. Run tests
python3 -m pytest tests/ -v
```

## Tool Versions

- Python: 3.11+
- pytest: 9.0.2
- No external dependencies required

## Evidence Index

| # | Deliverable | File | Proves |
|---|-------------|------|--------|
| 1 | Range manifest | `range/state.json` | Range built successfully |
| 2 | Candidate binding | `candidate.json` | D5 variant assignment |
| 3 | Health report | `range/health.json` | All checks passing |
| 4 | Source hashes | `output/provenance/pre-open-hashes.json` | Archive integrity |
| 5 | Versioned graph | `output/enumeration/graph.json` | 7 nodes, 9 edges |
| 6 | Edge validation | `output/enumeration/edge-validation.json` | 8 valid, 1 rejected |
| 7 | Stale edge explanation | `output/enumeration/edge-validation.json` | Rejection logic |
| 8 | Path graphs | `output/attack-paths.json` | 2 independent paths |
| 9 | Raw evidence locators | `output/attack-paths.json` | Source records |
| 10 | Proof-limit accounting | `output/attack-paths.json` | Limit compliance |
| 11 | Automation transcripts | `output/automation-*.json` | 3 clean runs |
| 12 | Cleanup results | `range/state.json` | Temporary objects removed |
| 13 | Graph diff before | `output/enumeration/graph-diff-before.json` | Pre-remediation state |
| 14 | Graph diff after | `output/remediation/graph-diff-after.json` | Post-remediation state |
| 15 | Negative path tests | `output/remediation/negative-retest-*.log` | Paths blocked |
| 16 | Detection rules | `output/detections/` | Positive + benign fixtures |

## Attack Paths

### Path 1: SPN Abuse → Service Token → Read Proof
- **Edge 1:** WriteSPN (candidate → svc-archive)
- **Edge 2:** CanAuthenticate (svc-archive → FILE01)
- **Edge 3:** ReadProof (svc-archive → archive-primary)
- **Proof:** `NF-AD1-3036faaf45086bf441f25cff1777`

### Path 2: GenericAll → Group Membership → Read Proof
- **Edge 1:** GenericAll (candidate → Archive Operators)
- **Edge 2:** MemberOf (candidate → Archive Operators)
- **Edge 3:** ReadProof (Archive Operators → archive-secondary)
- **Proof:** `NF-AD2-c07e006b267495929c79937edec4`

## Detection Rules

### Path 1 Detection (SPN Abuse)
- **Trigger:** `set-spn` + `request-service-token`
- **Result:** alert

### Path 2 Detection (Group Membership)
- **Trigger:** `add-group-member`
- **Result:** alert

## Remediation

- **Path 1:** Blocked at SPN abuse edge
- **Path 2:** Blocked at group membership edge
- **Health:** Legitimate access remains green
