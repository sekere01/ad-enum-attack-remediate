from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_act(assignment: Path, root: Path, operation: str) -> dict:
    result = subprocess.run(
        [sys.executable, "evidence/lab-source/portable_range.py", "act",
         "--assignment", str(assignment), "--root", str(root), operation],
        capture_output=True, text=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    output = {}

    r1 = run_act(args.assignment, args.root, "set-spn")
    r2 = run_act(args.assignment, args.root, "request-service-token")
    r3 = run_act(args.assignment, args.root, "read-proof-1")
    output["path_1"] = {
        "ok": r1["ok"] and r2["ok"] and r3["ok"],
        "steps": [r1, r2, r3],
        "proof": r3.get("proof"),
    }

    r4 = run_act(args.assignment, args.root, "add-group-member")
    r5 = run_act(args.assignment, args.root, "read-proof-2")
    output["path_2"] = {
        "ok": r4["ok"] and r5["ok"],
        "steps": [r4, r5],
        "proof": r5.get("proof"),
    }

    r6 = run_act(args.assignment, args.root, "cleanup")
    output["cleanup"] = {"ok": r6["ok"]}

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
