import pytest

from src.waypoint_store import WaypointStore, InvalidSlotError, SlotAlreadyRecordedError


def test_empty_store_has_no_recorded_slots():
    store = WaypointStore()
    assert store.is_recorded("start") is False
    assert store.is_recorded("target") is False
    assert store.get("start") is None
    assert store.get("target") is None


def test_record_start_stores_angles():
    store = WaypointStore()
    angles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    store.record("start", angles)
    assert store.is_recorded("start") is True
    assert store.get("start") == angles


def test_record_target_stores_angles():
    store = WaypointStore()
    angles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    store.record("target", angles)
    assert store.is_recorded("target") is True
    assert store.get("target") == angles


def test_record_invalid_slot_raises():
    store = WaypointStore()
    angles = [0.1] * 6
    with pytest.raises(InvalidSlotError):
        store.record("middle", angles)
    with pytest.raises(InvalidSlotError):
        store.record("", angles)


def test_record_wrong_dimension_raises():
    store = WaypointStore()
    with pytest.raises(ValueError):
        store.record("start", [0.1, 0.2, 0.3])  # too few
    with pytest.raises(ValueError):
        store.record("start", [0.1] * 7)  # too many


def test_record_overwrite_without_force_raises():
    store = WaypointStore()
    store.record("start", [0.1] * 6)
    with pytest.raises(SlotAlreadyRecordedError):
        store.record("start", [0.2] * 6)


def test_record_overwrite_with_force_succeeds():
    store = WaypointStore()
    store.record("start", [0.1] * 6)
    new_angles = [0.9] * 6
    store.record("start", new_angles, force=True)
    assert store.get("start") == new_angles


def test_slots_lists_valid_slot_names():
    store = WaypointStore()
    assert set(store.slots) == {"start", "target"}


def test_clear_resets_one_slot():
    store = WaypointStore()
    store.record("start", [0.1] * 6)
    store.record("target", [0.2] * 6)
    store.clear("start")
    assert store.is_recorded("start") is False
    assert store.is_recorded("target") is True
