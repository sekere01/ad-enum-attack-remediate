from src.remediation import remediate_path_1, remediate_path_2


def test_remediation_blocks_path_1():
    state = {"remediated": {"path_1": False, "path_2": False},
             "temporary": {"spn_added": False, "group_member_added": False, "service_token": False}}
    remediate_path_1(state)
    assert state["remediated"]["path_1"] is True
    assert state["temporary"]["spn_added"] is False


def test_remediation_blocks_path_2():
    state = {"remediated": {"path_1": False, "path_2": False},
             "temporary": {"spn_added": False, "group_member_added": False, "service_token": False}}
    remediate_path_2(state)
    assert state["remediated"]["path_2"] is True
    assert state["temporary"]["group_member_added"] is False
