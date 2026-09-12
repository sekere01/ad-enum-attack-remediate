# AD Enum Attack & Remediate

Offensive and defensive Active Directory enumeration, attack-path discovery, detection, and remediation toolkit.

## What It Does

1. **Enumerate** — Builds a graph of AD objects and relationships from an offline range
2. **Validate** — Checks edges for correctness, rejects stale/invalid ones
3. **Attack** — Discovers exploit paths (SPN abuse, group membership escalation)
4. **Detect** — Flags malicious activity with positive and benign detection rules
5. **Remediate** — Blocks attack paths while preserving legitimate access

## Quick Start

```bash
# Build the offline AD range
python3 -m src.graph_builder --root ad-range --out output/enumeration
python3 -m src.edge_validator --root ad-range --out output/enumeration

# Find attack paths
python3 -m src.path_finder --graph output/enumeration/graph.json \
  --start candidate-54206ab0 --targets archive-primary archive-secondary --out output

# Run detections
python3 -m src.detections --root ad-range --out output/detections

# Apply remediations
python3 -m src.remediation --assignment candidate.json --root ad-range

# Run all tests
python3 -m pytest tests/ -v
```

Or use the Makefile:

```bash
make enumerate    # build + validate graph
make attack       # run attack automation
make detect       # run detection rules
make remediate    # apply remediations
make test         # run test suite
```

## Project Structure

```
├── src/                    # Core modules
│   ├── automation.py       # Attack path automation
│   ├── detections.py       # Detection rule engine
│   ├── edge_validator.py   # Graph edge validation
│   ├── graph_builder.py    # AD object graph builder
│   ├── path_finder.py      # Attack path discovery
│   └── remediation.py      # Path remediation logic
├── tests/                  # Test suite
├── ad-range/               # Offline AD range data
│   ├── state.json          # Object state
│   ├── events.jsonl        # Event ledger
│   ├── manifest.json       # Range manifest
│   └── source-records.json # Source records
└── Makefile                # Build/test targets
```

## Requirements

- Python 3.11+
- pytest 9.0.2+
- No external dependencies

## Attack Paths Discovered

### Path 1: SPN Abuse → Service Token → Read Proof
- WriteSPN (candidate → svc-archive)
- CanAuthenticate (svc-archive → FILE01)
- ReadProof (svc-archive → archive-primary)

### Path 2: GenericAll → Group Membership → Read Proof
- GenericAll (candidate → Archive Operators)
- MemberOf (candidate → Archive Operators)
- ReadProof (Archive Operators → archive-secondary)

## Detection Rules

| Path | Trigger | Result |
|------|---------|--------|
| 1 (SPN Abuse) | `set-spn` + `request-service-token` | Alert |
| 2 (Group Membership) | `add-group-member` | Alert |

## Remediation

- **Path 1:** Blocked at SPN abuse edge
- **Path 2:** Blocked at group membership edge
- Legitimate access remains functional
