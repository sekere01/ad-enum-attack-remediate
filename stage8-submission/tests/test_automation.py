import subprocess
import json


def test_automation_runs_clean():
    result = subprocess.run(
        ["python3", "src/automation.py", "--assignment", "candidate.json", "--root", "range"],
        capture_output=True, text=True)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    output = json.loads(result.stdout)
    assert output["path_1"]["ok"] is True
    assert output["path_2"]["ok"] is True
    assert output["cleanup"]["ok"] is True


def test_automation_dynamic_resolution():
    with open("src/automation.py") as f:
        source = f.read()
    assert "S-1-5-21" not in source
    assert "candidate-v1" not in source
    assert "svc-archive-v1" not in source
    assert "archive-primary" not in source
