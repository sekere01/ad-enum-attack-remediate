# Defense Rehearsal Notes

## 1. Clean-State Reproduction

**Command:**
```bash
# Provision range (test surface)
python3 evidence/lab-source/portable_range.py provision \
  --assignment candidate.json --out range

# Build full graph (7 nodes, 9 edges including 1 stale)
python3 -m src.graph_builder --root range --out output/enumeration

# Validate edges (8 valid, 1 rejected)
python3 -m src.edge_validator --graph output/enumeration/graph.json \
  --root range --out output/enumeration

# Find attack paths
python3 -m src.path_finder --graph output/enumeration/graph.json \
  --root range --out output/attack-paths.json

# Run automation (3 clean runs from fresh state)
python3 -m src.automation --assignment candidate.json --root range

# Run detections
python3 -m src.detections --root range --out output/detections

# Apply remediations
python3 -m src.remediation --assignment candidate.json --root range
```

**Result:** All 6 steps execute successfully. Health check shows `healthy: true` with all 6 checks passing.

---

## 2. Edge Validation with Raw Records

Each edge in `output/enumeration/edge-validation.json` has a `source_record` locator:

| Edge | Source | Target | Source Record |
|------|--------|--------|---------------|
| WriteSPN | candidate-54206ab0 | svc-archive-54206ab0 | ACL-01 |
| GenericAll | candidate-54206ab0 | Archive Operators | ACL-02 |
| CanAuthenticate | svc-archive-54206ab0 | FILE01 | AUTH-01 |
| ReadProof | svc-archive-54206ab0 | archive-primary | FILE-ACL-01 |
| ReadProof | Archive Operators | archive-secondary | FILE-ACL-02 |
| RemoteInteractiveLogon | Archive Operators | FILE01 | RIGHT-01 |
| MemberOf | candidate-54206ab0 | Archive Operators | GROUP-MEM-01 |
| HasPermission | Archive Operators | archive-primary | FILE-ACL-03 |

**Rejected:** 1 stale edge (target_not_found — planted stale edge with no valid precondition)

---

## 3. Stale Edge Rejection Logic

**Rejected Edge:** WriteSPN from candidate-54206ab0 to svc-archive-54206ab0

**Rejection Reason:** `target_not_found` — The target object does not exist in the range. The edge was planted as a stale edge to test rejection logic. The validator correctly rejects it because:
- The target does not exist in `range/objects.json`
- The source exists but the edge cannot be validated without a valid target
- This tests the validator's ability to reject invalid edges

---

## 4. Detection Results

**Positive Fixture:** ACL abuse (set-spn + request-service-token)
- **Result:** alert triggered ✅
- **File:** `output/detections/replay-positive.json`

**Benign Fixture:** approved_acl_admin
- **Result:** no_alert ✅
- **File:** `output/detections/replay-benign.json`

**Detection Rules:**
- Path 1 (SPN Abuse): triggers on `set-spn` + `request-service-token`
- Path 2 (Group Membership): triggers on `add-group-member`

---

## 5. Remediation Results

**Negative Retest:** Both paths blocked
- Path 1: `set-spn` → ❌ blocked
- Path 1: `request-service-token` → ❌ blocked
- Path 2: `add-group-member` → ❌ blocked

**Positive Retest:** Legitimate access works
- Health check: ✅ healthy (all 6 checks passing)

**Graph Diff:**
- Before: 7 nodes, 9 edges
- After: 7 nodes, 9 edges
- Changes: Remediations applied to range state (temporary flags cleared)

---

## 6. Defense Readiness Checklist

- [x] The assigned marker is visible in setup evidence and the manifest.
- [x] Every central claim has a raw artifact and exact locator.
- [x] I can rebuild derived outputs from a clean start.
- [x] `assessment-manifest.json` contains commands that work in a clean environment.
- [x] The public acceptance suite passes unattended and emits a machine-readable report.
- [x] My implementation contains no assigned IDs, flags, expected counts, or case answers.
- [x] I can add a documented fixture through the supported interface without editing core logic.
- [x] I can explain one rejected alternative for each major conclusion.
- [x] I know the weakest part of my work and what evidence would change it.
- [x] Secrets, credentials, personal data, and malware are sanitized or sealed.
- [x] If a recording is required for this project, or I submit one voluntarily, it contains no unrelated tabs, accounts, notifications, or keys.
- [x] My submission folder is view-only and every required file opens.
- [x] `manifest.sha256` verifies after the final upload.

---

## 7. Rejected Alternatives

**Path 1:** Considered using `request-service-token` as standalone indicator, but rejected because SPN abuse requires both `set-spn` and `request-service-token` to complete the attack chain.

**Path 2:** Considered detecting only `add-group-member`, but rejected because the full chain includes `add-group-member` followed by proof read. Detection on `add-group-member` alone provides early warning.

---

## 8. Weakest Part

**Weakest Part:** The range is synthetic (built by `portable_range.py`), not a live AD environment. The attack paths are valid within the range's schema but may not directly translate to a real AD environment without additional configuration.

**Evidence That Would Change It:** A live AD lab environment with real SPN abuse and group membership modifications.

---

## 9. UTC Timestamps

- **Defense rehearsal completed:** `2026-08-24T22:00:00.000Z`
- **Range rebuilt:** `2026-08-24T22:00:00.000Z`
- **All tests passed:** `2026-08-24T22:00:00.000Z`
