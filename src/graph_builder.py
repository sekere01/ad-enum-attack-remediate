from __future__ import annotations
import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "2.0"


def build_graph(state: dict) -> dict:
    nodes = []
    for obj in state["objects"]:
        nodes.append({
            "id": obj["id"],
            "type": obj["type"],
            "name": obj["name"],
            "enabled": obj.get("enabled", True),
            "spns": obj.get("spns", []),
            "members": obj.get("members", []),
        })
    edges = []
    for rel in state["relations"]:
        edges.append({
            "source": rel["source"],
            "edge": rel["edge"],
            "target": rel["target"],
            "source_record": rel["source_record"],
            "stale": rel.get("stale", False),
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "binding": state.get("binding"),
        "marker": state.get("marker"),
        "variant": state.get("variant"),
        "nodes": nodes,
        "edges": edges,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    state = json.load(open(args.root / "state.json"))
    graph = build_graph(state)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "graph.json").write_text(json.dumps(graph, indent=2, sort_keys=True))
    print(json.dumps({"status": "ok", "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}))


if __name__ == "__main__":
    main()
