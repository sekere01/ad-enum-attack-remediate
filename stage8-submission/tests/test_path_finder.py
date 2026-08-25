from src.path_finder import find_paths


def test_find_two_independent_paths():
    graph = {
        "edges": [
            {"source": "candidate-v1", "edge": "WriteSPN", "target": "svc-archive-v1",
             "source_record": "ACL-01", "stale": False},
            {"source": "svc-archive-v1", "edge": "ReadProof", "target": "archive-primary",
             "source_record": "FILE-ACL-01", "stale": False},
            {"source": "candidate-v1", "edge": "GenericAll", "target": "Archive Operators",
             "source_record": "ACL-02", "stale": False},
            {"source": "Archive Operators", "edge": "ReadProof", "target": "archive-secondary",
             "source_record": "FILE-ACL-02", "stale": False},
        ],
        "nodes": [
            {"id": "U-01", "type": "user", "name": "candidate-v1"},
            {"id": "U-02", "type": "user", "name": "svc-archive-v1"},
            {"id": "G-01", "type": "group", "name": "Archive Operators"},
            {"id": "P-01", "type": "proof", "name": "archive-primary"},
            {"id": "P-02", "type": "proof", "name": "archive-secondary"},
        ]
    }
    paths = find_paths(graph, "candidate-v1", ["archive-primary", "archive-secondary"])
    assert len(paths) == 2
    assert paths[0]["proof"] != paths[1]["proof"]
    assert set(paths[0]["edge_names"]) != set(paths[1]["edge_names"])


def test_paths_diverge_at_credential_or_acl():
    """At least one path must combine credential abuse with ACL/delegation."""
    graph = {
        "edges": [
            {"source": "candidate-v1", "edge": "WriteSPN", "target": "svc-archive-v1",
             "source_record": "ACL-01", "stale": False},
            {"source": "svc-archive-v1", "edge": "ReadProof", "target": "archive-primary",
             "source_record": "FILE-ACL-01", "stale": False},
            {"source": "candidate-v1", "edge": "GenericAll", "target": "Archive Operators",
             "source_record": "ACL-02", "stale": False},
            {"source": "Archive Operators", "edge": "ReadProof", "target": "archive-secondary",
             "source_record": "FILE-ACL-02", "stale": False},
        ], "nodes": []
    }
    paths = find_paths(graph, "candidate-v1", ["archive-primary", "archive-secondary"])
    assert "WriteSPN" in paths[0]["edge_names"] or "WriteSPN" in paths[1]["edge_names"]
