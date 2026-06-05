from dataclasses import dataclass, replace
from typing import Literal

from .waypoint_store import WaypointStore

IDLE = "IDLE"
AT_TARGET = "AT_TARGET"
Status = Literal["IDLE", "AT_TARGET"]

OPTION_READ = 1
OPTION_RECORD = 2
OPTION_RUN_WAYPOINT = 3
OPTION_RETURN = 4
OPTION_ESTOP = 0

ALL_OPTIONS = (OPTION_READ, OPTION_RECORD, OPTION_RUN_WAYPOINT, OPTION_RETURN, OPTION_ESTOP)
OPTION_LABELS = {
    OPTION_READ: "读取关节角度",
    OPTION_RECORD: "记录关节角度",
    OPTION_RUN_WAYPOINT: "运行 waypoint",
    OPTION_RETURN: "返回起始位置",
    OPTION_ESTOP: "电子急停",
}


@dataclass(frozen=True)
class MenuState:
    status: Status = IDLE


def is_option_available(option: int, state: MenuState, store: WaypointStore) -> bool:
    if option not in ALL_OPTIONS:
        raise ValueError(f"unknown option: {option}")
    if option in (OPTION_READ, OPTION_RECORD, OPTION_ESTOP):
        return True
    if option == OPTION_RUN_WAYPOINT:
        return store.is_recorded("target")
    if option == OPTION_RETURN:
        return state.status == AT_TARGET and store.is_recorded("start")
    return False


def transition_after(option: int, state: MenuState) -> MenuState:
    if option == OPTION_RUN_WAYPOINT:
        return replace(state, status=AT_TARGET)
    if option == OPTION_RETURN:
        return replace(state, status=IDLE)
    return state


def render_menu(state: MenuState, store: WaypointStore) -> str:
    lines = ["=== 测试菜单 ==="]
    for opt in ALL_OPTIONS:
        if is_option_available(opt, state, store):
            lines.append(f"{opt}) {OPTION_LABELS[opt]}")
    lines.append(f"[状态: {state.status} | start: {'已记录' if store.is_recorded('start') else '未记录'} | target: {'已记录' if store.is_recorded('target') else '未记录'}]")
    return "\n".join(lines)
