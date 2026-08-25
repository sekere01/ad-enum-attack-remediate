from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path


def remediate_path_1(state: dict) -> None:
    state["remediated"]["path_1"] = True
    state["temporary"]["spn_added"] = False
    state["temporary"]["service_token"] = False


def remediate_path_2(state: dict) -> None:
    state["remediated"]["path_2"] = True
    state["temporary"]["group_member_added"] = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    r1 = subprocess.run(
        [sys.executable, "evidence/lab-source/portable_range.py", "act",
         "--assignment", str(args.assignment), "--root", str(args.root), "remediate-path-1"],
        capture_output=True, text=True)
    r2 = subprocess.run(
        [sys.executable, "evidence/lab-source/portable_range.py", "act",
         "--assignment", str(args.assignment), "--root", str(args.root), "remediate-path-2"],
        capture_output=True, text=True)

    print(json.dumps({
        "remediate_path_1": json.loads(r1.stdout),
        "remediate_path_2": json.loads(r2.stdout),
    }, indent=2))


if __name__ == "__main__":
    main()
