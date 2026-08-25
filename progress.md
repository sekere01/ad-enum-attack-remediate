# Stage 8: Break and Repair the Directory Control Plane — Progress Tracker

> Reference the implementation plan at `evidence/plan` for detailed instructions.

---

## Phase 0: Repository & Provenance Setup

- [x] 0.1 Initialize git repository
- [x] 0.2 Record pre-open hashes (SHA-256 before extraction)

---

## Phase 1: Build & Checkpoint (Mon Morning)

- [ ] 1.1 Obtain and validate candidate JSON (PRIVATE, never committed)
- [ ] 1.2 Generate offline range via `portable_range.py build`
- [ ] 1.3 Health check — all 6 checks green
- [ ] 1.4 Create Makefile (single entry command)
- [ ] 1.5 Commit Phase 1 checkpoint

---

## Phase 2: Collect & Challenge Graph (Mon Afternoon)

- [ ] 2.1 Build graph builder (versioned with `schema_version`)
- [ ] 2.2 Build edge validator (all public test edges: group, ACL, stale, delegation, disabled)
- [ ] 2.3 Validate 8+ edges from raw records, reject stale edge with explanation
- [ ] 2.4 Commit Phase 2

---

## Phase 3: Prove & Automate Paths (Tue–Wed)

- [ ] 3.1 Build path finder (independent paths with divergence point)
- [ ] 3.2 Validate two independent attack paths with proof limit accounting
- [ ] 3.3 Build automation (dynamic resolution, no hardcoded values)
- [ ] 3.4 Run 3 consecutive clean automation tests (rebuild between each)
- [ ] 3.5 Commit Phase 3

---

## Phase 4: Detect, Clean & Remediate (Thursday)

- [ ] 4.1 Export event ledger to `output/windows-events/`
- [ ] 4.2 Write detection rules (positive + benign fixtures)
- [ ] 4.3 Remediate both paths (graph diff before/after)
- [ ] 4.4 Run negative retests (attacks fail at intended edges)
- [ ] 4.5 Run positive legitimate-access tests (health stays green)
- [ ] 4.6 Commit Phase 4

---

## Phase 5: Rehearse Defense (Fri Morning)

- [ ] 5.1 Defense rehearsal checklist
- [ ] 5.2 Prepare credential handling (fill template, sign)

---

## Phase 6: Package & Submit (Fri by 18:10 WAT)

- [ ] 6.1 Create runbook (`README.md` with reproduction steps)
- [ ] 6.2 Assemble 16 deliverables in `submission/`
- [ ] 6.3 Fill `evidence-index.csv` (full evidence standard)
- [ ] 6.4 Fill `assessment-manifest.json` (all fields)
- [ ] 6.5 Fill `integrity-attestation.md` (with AI declaration)
- [ ] 6.6 Generate `manifest.sha256`
- [ ] 6.7 Final verification (all 10 public tests pass)
- [ ] 6.8 Upload to Google Drive (`UBI-ID-STAGE_8`, view-only)
- [ ] 6.9 Final git commit and record frozen commit hash

---

## Status Log

| Date | Event | Detail | Outcome |
|------|-------|--------|---------|
| 2026-08-24 | Plan created | Revised plan addressing 14 compliance gaps | Saved to `evidence/plan` |
| 2026-08-24 | Progress tracker created | Task tracker initialized | Saved to `progress.md` |
| 2026-08-25 | Phase 0 complete | Git repo initialized, pre-open hashes recorded | Commit f2fca42, d776184 |
| 2026-08-25 | Candidate JSON validated | Variant D5, marker UBI-A8-E7C1EEB30702 | `candidate.json` gitignored |
| 2026-08-25 | Evidence marked read-only | `chmod -R a-w evidence/` | Verified |
