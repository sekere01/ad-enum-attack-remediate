from __future__ import annotations
import argparse
import json
from collections import deque
from pathlib import Path


def find_paths(graph: dict, start: str, targets: list[str]) -> list[dict]:
    edges = [e for e in graph["edges"] if not e.get("stale", False)]

    adj: dict[str, list[dict]] = {}
    for e in edges:
        adj.setdefault(e["source"], []).append(e)

    results = []
    for target in targets:
        path = bfs(adj, start, target)
        if path:
            results.append(path)
    return results


def bfs(adj: dict[str, list[dict]], start: str, goal: str) -> dict | None:
    queue = deque([(start, [])])
    visited = {start}

    while queue:
        node, path = queue.popleft()
        if node == goal:
            edge_names = [e["edge"] for e in path]
            source_records = [e["source_record"] for e in path]
            return {
                "proof": goal,
                "edge_names": edge_names,
                "raw_evidence_locators": source_records,
                "edges": path,
            }
        for edge in adj.get(node, []):
            nxt = edge["target"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [edge]))
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--start", type=str, required=True)
    parser.add_argument("--targets", nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    graph = json.load(open(args.graph))
    paths = find_paths(graph, args.start, args.targets)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "attack-paths.json").write_text(json.dumps({
        "path_1": paths[0] if len(paths) > 0 else None,
        "path_2": paths[1] if len(paths) > 1 else None,
        "independent": len(paths) == 2 and set(paths[0]["edge_names"]) != set(paths[1]["edge_names"]),
        "divergence_edge_credential_or_acl": any(
            "WriteSPN" in p.get("edge_names", []) for p in paths
        ),
    }, indent=2))
    print(json.dumps({"paths_found": len(paths)}))


if __name__ == "__main__":
    main()
