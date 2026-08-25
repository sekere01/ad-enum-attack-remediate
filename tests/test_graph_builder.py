import json
from src.graph_builder import build_graph


def test_build_graph_loads_objects():
    state = json.load(open("range/state.json"))
    graph = build_graph(state)
    assert len(graph["nodes"]) >= 7
    assert len(graph["edges"]) >= 8


def test_build_graph_has_schema_version():
    state = json.load(open("range/state.json"))
    graph = build_graph(state)
    assert "schema_version" in graph
    assert graph["schema_version"] == "2.0"


def test_build_graph_no_hardcoded_identifiers():
    with open("src/graph_builder.py") as f:
        source = f.read()
    assert "S-1-5-21" not in source
    assert "candidate-v1" not in source
    assert "svc-archive-v1" not in source
