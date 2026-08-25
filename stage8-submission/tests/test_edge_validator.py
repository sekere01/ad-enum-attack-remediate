from src.edge_validator import validate_edges, reject_stale_edge


def test_validate_real_edges():
    edges = [{"source": "candidate-v1", "edge": "WriteSPN", "target": "svc-archive-v1",
              "source_record": "ACL-01", "stale": False}]
    source_records = {"ACL-01": True}
    result = validate_edges(edges, source_records)
    assert len(result["validated"]) == 1


def test_reject_stale_edge():
    edges = [{"source": "candidate-v1", "edge": "GenericAll", "target": "deleted-group",
              "source_record": "STALE-01", "stale": True}]
    result = validate_edges(edges, {})
    assert len(result["rejected"]) == 1


def test_edge_delegation_valid():
    edges = [{"source": "svc-archive-v1", "edge": "AllowedToDelegate", "target": "FILE01",
              "source_record": "DELEG-01", "stale": False}]
    result = validate_edges(edges, {"DELEG-01": True})
    assert len(result["validated"]) == 1


def test_edge_disabled_reject():
    edges = [{"source": "admin", "edge": "HasSession", "target": "disabled-user",
              "source_record": "SESS-01", "stale": False, "account_enabled": False}]
    result = validate_edges(edges, {"SESS-01": True})
    assert len(result["rejected"]) >= 1
