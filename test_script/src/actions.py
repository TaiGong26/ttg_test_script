import threading
import time
from typing import Callable, Protocol

from .menu import (
    MenuState,
    OPTION_ESTOP,
    OPTION_READ,
    OPTION_RECORD,
    OPTION_RETURN,
    OPTION_RUN_WAYPOINT,
    transition_after,
)
from .waypoint_store import (
    InvalidSlotError,
    SlotAlreadyRecordedError,
    WaypointStore,
)

READ_HZ = 10
READ_PERIOD = 1.0 / READ_HZ


class ArmLike(Protocol):
    def get_joint_angles(self): ...
    def move_j(self, angles: list[float]) -> None: ...
    def electronic_emergency_stop(self) -> None: ...
    def disable(self) -> None: ...


ReadAnglesFn = Callable[[], list[float] | None]
InputFn = Callable[[str], str]


def _read_current_angles(arm: ArmLike) -> list[float] | None:
    sample = arm.get_joint_angles()
    if sample is None:
        return None
    msg = getattr(sample, "msg", sample)
    if isinstance(msg, (list, tuple)):
        return list(msg)
    return None


def do_read(
    arm: ArmLike,
    store: WaypointStore,
    state: MenuState,
    read_input_fn: InputFn = input,
    read_angles_fn: ReadAnglesFn | None = None,
) -> MenuState:
    if read_angles_fn is None:
        read_angles_fn = lambda: _read_current_angles(arm)
    stop = threading.Event()

    def wait_for_enter() -> None:
        try:
            read_input_fn("")
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            stop.set()

    waiter = threading.Thread(target=wait_for_enter, daemon=True)
    waiter.start()
    print("[读取模式] 按回车退出,持续打印关节角度:")
    try:
        while not stop.is_set():
            angles = read_angles_fn()
            if angles is not None:
                print(f"  joints: {[round(a, 4) for a in angles]}")
            else:
                print("  joints: <no data>")
            stop.wait(READ_PERIOD)
    finally:
        stop.set()
    print("[读取模式] 退出")
    return state


def do_record(
    arm: ArmLike,
    store: WaypointStore,
    state: MenuState,
    read_input_fn: InputFn = input,
) -> MenuState:
    print("记录到哪个位置? 1) 起始位置  2) target")
    choice = read_input_fn("选择 (1/2): ").strip()
    slot = "start" if choice == "1" else "target" if choice == "2" else None
    if slot is None:
        print("无效选择")
        return state
    if store.is_recorded(slot):
        confirm = read_input_fn(f"{slot} 已记录,覆盖? (y/N): ").strip().lower()
        if confirm != "y":
            print("已取消")
            return state
        force = True
    else:
        force = False
    angles = _read_current_angles(arm)
    if angles is None:
        print("读取关节角度失败,未记录")
        return state
    try:
        store.record(slot, angles, force=force)
        print(f"已记录 {slot}: {[round(a, 4) for a in angles]}")
    except (InvalidSlotError, SlotAlreadyRecordedError, ValueError) as e:
        print(f"记录失败: {e}")
    return state


def do_run_waypoint(
    arm: ArmLike,
    store: WaypointStore,
    state: MenuState,
) -> MenuState:
    if not store.is_recorded("target"):
        print("target 未记录,无法运行 waypoint")
        return state
    target = store.get("target")
    assert target is not None
    print(f"运行到 target: {[round(a, 4) for a in target]}")
    arm.move_j(target)
    print("已到达 target")
    return transition_after(OPTION_RUN_WAYPOINT, state)


def do_return_to_start(
    arm: ArmLike,
    store: WaypointStore,
    state: MenuState,
) -> MenuState:
    if state.status != "AT_TARGET":
        print("当前不在 target,无法返回")
        return state
    if not store.is_recorded("start"):
        print("start 未记录,无法返回")
        return state
    start = store.get("start")
    assert start is not None
    print(f"返回到 start: {[round(a, 4) for a in start]}")
    arm.move_j(start)
    print("已返回 start")
    return transition_after(OPTION_RETURN, state)


def do_estop(arm: ArmLike, store: WaypointStore, state: MenuState) -> MenuState:
    print("[电子急停] 触发 electronic_emergency_stop()")
    arm.electronic_emergency_stop()
    print("[电子急停] 已触发,如需继续请先手动重新使能")
    return state


ACTION_DISPATCH = {
    OPTION_READ: do_read,
    OPTION_RECORD: do_record,
    OPTION_RUN_WAYPOINT: do_run_waypoint,
    OPTION_RETURN: do_return_to_start,
    OPTION_ESTOP: do_estop,
}
