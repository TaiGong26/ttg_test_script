import os
import signal
import sys
import time

from pyAgxArm import AgxArmFactory, create_agx_arm_config

from src.actions import ACTION_DISPATCH
from src.menu import (
    ALL_OPTIONS,
    MenuState,
    is_option_available,
    render_menu,
)
from src.waypoint_store import WaypointStore


def build_arm(robot: str = "nero", channel: str = "can0"):
    cfg = create_agx_arm_config(robot=robot, comm="can", channel=channel, interface="socketcan")
    arm = AgxArmFactory.create_arm(cfg)
    return arm


def wait_until_enabled(arm) -> None:
    while not arm.enable():
        time.sleep(0.1)
        print("waiting... enable robot")


def install_sigint_handler(arm) -> None:
    def _handler(signum, frame):
        print("\n[SIGINT] 立即断电: 调用 disable()")
        try:
            arm.disable()
        except Exception as e:
            print(f"[SIGINT] disable 失败: {e}")
        os._exit(130)

    signal.signal(signal.SIGINT, _handler)


def parse_choice(raw: str) -> int | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def main() -> None:
    arm = build_arm()
    arm.connect()
    arm.set_normal_mode()
    wait_until_enabled(arm)
    install_sigint_handler(arm)

    store = WaypointStore()
    state = MenuState()
    try:
        while True:
            print()
            print(render_menu(state, store))
            choice = parse_choice(input("选择: "))
            if choice is None:
                print("无效输入")
                continue
            if choice not in ALL_OPTIONS:
                print("无效选项")
                continue
            if not is_option_available(choice, state, store):
                print("该选项当前不可用")
                continue
            handler = ACTION_DISPATCH[choice]
            state = handler(arm, store, state)
    except KeyboardInterrupt:
        # 兜底:实际 SIGINT 已被自定义 handler 拦截,这里只是双保险
        try:
            arm.disable()
        finally:
            os._exit(130)
    except Exception as e:
        print(f"[main] 异常: {e}")
        try:
            arm.disable()
        finally:
            sys.exit(1)


if __name__ == "__main__":
    main()
