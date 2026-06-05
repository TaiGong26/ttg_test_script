import pytest

from src.menu import (
    OPTION_READ,
    OPTION_RECORD,
    OPTION_RUN_WAYPOINT,
    OPTION_RETURN,
    OPTION_ESTOP,
    MenuState,
    IDLE,
    AT_TARGET,
    is_option_available,
    transition_after,
    render_menu,
)
from src.waypoint_store import WaypointStore


def test_idle_no_records_only_basics_available():
    state = MenuState()
    assert is_option_available(OPTION_READ, state, WaypointStore()) is True
    assert is_option_available(OPTION_RECORD, state, WaypointStore()) is True
    assert is_option_available(OPTION_RUN_WAYPOINT, state, WaypointStore()) is False
    assert is_option_available(OPTION_RETURN, state, WaypointStore()) is False
    assert is_option_available(OPTION_ESTOP, state, WaypointStore()) is True


def test_idle_with_target_recorded_run_waypoint_available():
    state = MenuState()
    store = WaypointStore()
    store.record("target", [0.1] * 6)
    assert is_option_available(OPTION_RUN_WAYPOINT, state, store) is True
    assert is_option_available(OPTION_RETURN, state, store) is False


def test_at_target_both_recorded_return_available():
    state = MenuState(status=AT_TARGET)
    store = WaypointStore()
    store.record("start", [0.1] * 6)
    store.record("target", [0.2] * 6)
    assert is_option_available(OPTION_RETURN, state, store) is True


def test_at_target_missing_start_return_unavailable():
    state = MenuState(status=AT_TARGET)
    store = WaypointStore()
    store.record("target", [0.2] * 6)
    assert is_option_available(OPTION_RETURN, state, store) is False


def test_run_waypoint_transitions_idle_to_at_target():
    state = MenuState(status=IDLE)
    new_state = transition_after(OPTION_RUN_WAYPOINT, state)
    assert new_state.status == AT_TARGET


def test_return_transitions_at_target_to_idle():
    state = MenuState(status=AT_TARGET)
    new_state = transition_after(OPTION_RETURN, state)
    assert new_state.status == IDLE


def test_read_record_estop_do_not_change_state():
    state = MenuState(status=IDLE)
    for opt in (OPTION_READ, OPTION_RECORD, OPTION_ESTOP):
        assert transition_after(opt, state).status == IDLE


def test_invalid_option_raises():
    with pytest.raises(ValueError):
        is_option_available(99, MenuState(), WaypointStore())


def test_render_menu_idle_includes_return_not_run():
    store = WaypointStore()
    store.record("target", [0.1] * 6)
    text = render_menu(MenuState(status=IDLE), store)
    assert "读取关节角度" in text
    assert "记录关节角度" in text
    assert "运行 waypoint" in text
    assert "电子急停" in text
    assert "返回起始位置" not in text


def test_render_menu_at_target_includes_return():
    store = WaypointStore()
    store.record("start", [0.1] * 6)
    store.record("target", [0.2] * 6)
    text = render_menu(MenuState(status=AT_TARGET), store)
    assert "返回起始位置" in text
