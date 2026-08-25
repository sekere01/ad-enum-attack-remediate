from __future__ import annotations
import argparse
import json
from pathlib import Path


def detect_path_1(events: list[dict]) -> bool:
    actions = [e["action"] for e in events if e.get("result") == "success"]
    return "set-spn" in actions and "request-service-token" in actions


def detect_path_2(events: list[dict]) -> bool:
    actions = [e["action"] for e in events if e.get("result") == "success"]
    return "add-group-member" in actions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    events = []
    with open(args.root / "events.jsonl") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    path_1_alert = detect_path_1(events)
    path_2_alert = detect_path_2(events)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "detection-results.json").write_text(json.dumps({
        "path_1_alert": path_1_alert,
        "path_2_alert": path_2_alert,
        "total_events": len(events),
    }, indent=2))
    print(json.dumps({"path_1_alert": path_1_alert, "path_2_alert": path_2_alert}))


if __name__ == "__main__":
    main()
