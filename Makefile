.PHONY: provision build health enumerate attack detect remediate test package clean

ASSIGNMENT ?= candidate.json
RANGE_DIR ?= range

provision:
	@test -f $(ASSIGNMENT) || (echo "ERROR: $(ASSIGNMENT) not found" && exit 1)
	@python3 -c "import json; d=json.load(open('$(ASSIGNMENT)')); assert d.get('project')=='EH-A4-PORTABLE'"
	@echo "PASS: candidate JSON validated"

build:
	python3 evidence/lab-source/portable_range.py build --assignment $(ASSIGNMENT) --out $(RANGE_DIR)

health:
	python3 evidence/lab-source/portable_range.py health --root $(RANGE_DIR)

enumerate:
	python3 -m src.graph_builder --root $(RANGE_DIR) --out output/enumeration
	python3 -m src.edge_validator --root $(RANGE_DIR) --out output/enumeration

attack:
	python3 src/automation.py --assignment $(ASSIGNMENT) --root $(RANGE_DIR)

detect:
	python3 -m src.detections --root $(RANGE_DIR) --out output/detections

remediate:
	python3 -m src.remediation --assignment $(ASSIGNMENT) --root $(RANGE_DIR)

test:
	python3 -m pytest tests/ -v --tb=short

package:
	python3 src/package.py --src . --dst submission

clean:
	rm -rf range/ output/ submission/ __pycache__/
