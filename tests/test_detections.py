from src.detections import detect_path_1, detect_path_2


def test_detect_path_1_positive():
    events = [{"action": "set-spn", "result": "success"},
              {"action": "request-service-token", "result": "success"}]
    assert detect_path_1(events) is True


def test_detect_path_1_benign():
    events = [{"action": "approved_acl_admin", "result": "success"}]
    assert detect_path_1(events) is False


def test_detect_path_2_positive():
    events = [{"action": "add-group-member", "result": "success"}]
    assert detect_path_2(events) is True


def test_detect_path_2_benign():
    events = [{"action": "approved_group_management", "result": "success"}]
    assert detect_path_2(events) is False
