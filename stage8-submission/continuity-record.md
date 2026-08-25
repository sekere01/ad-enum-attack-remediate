# Continuity Record — UBI Stage 8

## 1. Prior-Stage Component Reused

- **Previous Stage**: Stage 7 (IAM attack chain as code)
- **Previous Stage Commit**: `6d5559c`
- **Components adapted from Stage 7 `iam_chain/`**:

| Stage 7 Module | Stage 8 Module | Adaptation |
|---|---|---|
| Pattern: `graph_builder.py` | `src/graph_builder.py` | New graph builder for AD range (pattern reuse only, no imports) |
| Pattern: `edge_validator.py` | `src/edge_validator.py` | New edge validator for AD edges (pattern reuse only, no imports) |
| Pattern: `path_finder.py` | `src/path_finder.py` | New path finder for AD attack paths (pattern reuse only, no imports) |
| Pattern: `automation.py` | `src/automation.py` | New automation for AD range (pattern reuse only, no imports) |
| Pattern: `detections.py` | `src/detections.py` | New detections for AD events (pattern reuse only, no imports) |
| Pattern: `remediation.py` | `src/remediation.py` | New remediation for AD paths (pattern reuse only, no imports) |

## 2. Interface Consumed and Extensions

### Reused interfaces (pattern-only, no direct imports)

- Graph construction pattern: objects → nodes, relations → edges
- Edge validation pattern: source_record locator, stale rejection
- Path discovery pattern: BFS from foothold to proof objects
- Automation pattern: dynamic resolution, clean-state execution
- Detection pattern: positive + benign fixtures
- Remediation pattern: graph diff before/after

### Extended interfaces

- `graph_builder.py`: Added `schema_version` field, AD-specific node types (User, Group, Computer, SPN, ProofObject)
- `edge_validator.py`: Added stale edge rejection with `target_not_found` precondition
- `path_finder.py`: Added proof-limit accounting, independent path discovery
- `automation.py`: Added `portable_range.py act` integration, dynamic identifier resolution
- `detections.py`: Added event-sequence detection for AD-specific actions
- `remediation.py`: Added graph diff before/after, negative retest validation

### New interfaces

- `src/graph_builder.py`: AD-specific graph construction from `range/state.json`
- `src/edge_validator.py`: AD-specific edge validation with raw record locators
- `src/path_finder.py`: AD-specific BFS path finder with proof-limit accounting
- `src/automation.py`: AD-specific automation via `portable_range.py act`
- `src/detections.py`: AD-specific event-sequence detection
- `src/remediation.py`: AD-specific remediation with graph diff

## 3. Provenance Preserved

- JSONL event format retained from Stage 7 pattern
- Evidence locator format: `ACL-01`, `FILE-ACL-01`, `AUTH-01`, etc.
- Graph schema_version field for version tracking
- All attack steps record source_record for raw evidence linking
- Proof-limit accounting for each path

## 4. Migration Record

| Original (Stage 7) | Stage 8 Adaptation | Reason |
|---|---|---|
| AWS IAM graph (roles, policies, trust) | AD graph (users, groups, computers, SPNs, ACLs) | Different directory service |
| CloudTrail events | AD event logs | Different audit source |
| STS role assumption | Kerberos service tokens | Different authentication mechanism |
| S3 bucket policies | AD ACLs | Different access control model |
| Lambda function invocation | Remote interactive logon | Different execution mechanism |
| IAM policy remediation | AD group membership removal | Different remediation mechanism |

## 5. Hand-off to Stage 9

- **AD graph schema** (`graph.json`): 7 nodes, 9 edges (8 valid + 1 stale), schema_version 2.0
- **Edge evidence format** (`edge-validation.json`): source_record locators for each validated edge
- **Attack path format** (`attack-paths.json`): 2 independent paths with proof-limit accounting
- **Detection rules** (`detections/`): 2 event-sequence detections with positive/benign fixtures
- **Remediation records** (`remediation/`): graph diff before/after, negative retest logs
- **Automation transcripts** (`automation/`): 3 clean runs from fresh state
