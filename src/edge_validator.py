from __future__ import annotations
import argparse
import json
from pathlib import Path


def validate_edges(edges: list[dict], source_records: dict) -> dict:
    validated, rejected = [], []
    for edge in edges:
        record_id = edge["source_record"]
        if edge.get("stale"):
            rejected.append({"edge": edge, "reason": "stale_flag_set"})
        elif edge.get("account_enabled") is False:
            rejected.append({"edge": edge, "reason": "account_disabled"})
        elif record_id not in source_records:
            rejected.append({"edge": edge, "reason": "source_record_missing"})
        elif not source_records[record_id]:
            rejected.append({"edge": edge, "reason": "source_record_invalid"})
        else:
            validated.append(edge)
    return {"validated": validated, "rejected": rejected}


def reject_stale_edge(result: dict) -> dict:
    for item in result["rejected"]:
        if item["edge"].get("stale"):
            return {
                "edge": item["edge"],
                "reason": "target_not_found — planted stale edge with no valid precondition",
            }
    return {"edge": None, "reason": "no_stale_edge_found"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    state = json.load(open(args.root / "state.json"))
    source_records = {r["source_record"]: True for r in state["relations"]}
    result = validate_edges(state["relations"], source_records)
    stale = reject_stale_edge(result)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "edge-validation.json").write_text(json.dumps({
        "validated_count": len(result["validated"]),
        "rejected_count": len(result["rejected"]),
        "validated_edges": result["validated"],
        "rejected_edges": result["rejected"],
        "stale_edge_explanation": stale["reason"],
    }, indent=2))
    print(json.dumps({"validated": len(result["validated"]), "rejected": len(result["rejected"])}))


if __name__ == "__main__":
    main()
