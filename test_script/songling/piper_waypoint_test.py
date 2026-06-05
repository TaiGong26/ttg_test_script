#!/usr/bin/env python3
"""Record and execute two joint-space waypoints (target, home) for a Nero arm.

Usage:
    python waypoint_test.py --record     # record target + home joint angles (robot stays disabled)
    python waypoint_test.py --execute    # execute target -> home with manual Enter confirmation
    python waypoint_test.py --show       # print the currently recorded waypoints
"""

import argparse
import json
import sys
import time
from pathlib import Path

from pyAgxArm import create_agx_arm_config, AgxArmFactory

WAYPOINTS_FILE = Path.cwd() / "waypoints.json"
"""
ROBOT_CFG = create_agx_arm_config(
    robot="piper", comm="can", channel="can_right", interface="socketcan"
)
"""


SPEED_PERCENT = 30
MOTION_TIMEOUT_S = 5.0
MOTION_POLL_S = 0.1

# 等待机械臂运动完成，检查 motion_status == 0
def wait_motion_done(robot, timeout=MOTION_TIMEOUT_S, poll=MOTION_POLL_S):
    start = time.monotonic()
    while True:
        status = robot.get_arm_status()
        if status is not None and getattr(status.msg, "motion_status", None) == 0:
            return True
        
        # timeout check
        
        if time.monotonic() - start > timeout:
            return True
        time.sleep(poll)


def wait_enabled(robot, poll=0.1):

    while not robot.enable(255):
        time.sleep(poll)
        print("waiting... enable robot")
    print(f"Robot enabled {robot.enable()}")

# 记录目标和初始位置的关节角度，保存到 waypoints.json 文件中
def record(robot):
    # Recording requires a live connection (to read joint angles) but the arm
    # must stay disabled so the user can move it by hand.
    robot.disable()
    time.sleep(0.3)
    

    print("Move the arm to the TARGET position, then press Enter to capture.")
    
    # input()
    # targets = list(robot.get_joint_angles().msg)
    # print(f"  target = {targets}")
    
    targets = []
    for i in range(3):
    
        # print(f"pos{i}{robot.get_joint_angles()}")
        # time.sleep(0.5)
        input()
        target = list(robot.get_joint_angles().msg)
        print(f"  target = {target}")
        targets.append(target)

    print("Move the arm to the HOME position, then press Enter to capture.")
    input()
    home = list(robot.get_joint_angles().msg)
    print(f"  home   = {home}")

    WAYPOINTS_FILE.write_text(
        json.dumps({"target": targets, "home": home}, indent=2)
    )
    print(f"Saved to {WAYPOINTS_FILE}")

DATA = json.loads(WAYPOINTS_FILE.read_text())
HOME = DATA["home"]

# 执行记录的目标和初始位置，先移动到目标位置，等待用户确认后再移动回初始位置
def execute(robot):
    data = json.loads(WAYPOINTS_FILE.read_text())
    target, home = data["target"], data["home"]
    
    #robot.set_normal_mode()
    wait_enabled(robot)
    time.sleep(0.5)
    robot.set_speed_percent(SPEED_PERCENT)

        
    while True:
        print("Press Enter to continue to next target (Ctrl+C to abort).")
        
        for t in target:
            
            print(f"Moving to TARGET: {t}")
            robot.move_j(t)

            time.sleep(3)
        


def show():
    data = json.loads(WAYPOINTS_FILE.read_text())
    target, home = data["target"], data["home"]
    print(f"Recorded waypoints ({WAYPOINTS_FILE}):")
    print(f"  target: {target}")
    print(f"  home:   {home}")

# 解析命令行参数，要求用户选择 --record 或 --execute 其中一个选项
def parse_args():
    parser = argparse.ArgumentParser(
        description="Record and execute Nero arm waypoints."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record", action="store_true", help="Record target and home joint angles.")
    group.add_argument("--execute", action="store_true", help="Execute the recorded waypoints.")
    parser.add_argument("--can", default="can0", help="CAN interface to use.")
    group.add_argument("--show", action="store_true", help="Print the currently recorded waypoints.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.show:
        if not WAYPOINTS_FILE.exists():
            print(f"ERROR: {WAYPOINTS_FILE} not found. Run --record first.")
            sys.exit(1)
        show()
        return

    if args.execute and not WAYPOINTS_FILE.exists():
        print(f"ERROR: {WAYPOINTS_FILE} not found. Run --record first.")
        sys.exit(1)

    try:
        ROBOT_CFG = create_agx_arm_config(robot="piper", comm="can", channel=args.can, interface="socketcan")
        robot = AgxArmFactory.create_arm(ROBOT_CFG)
        robot.connect()
        #robot.set_normal_mode()
        wait_enabled(robot)
        print(robot.is_connected())
    except Exception as e:
        print(f"Failed to connect to robot: {e}")
        sys.exit(1)

    try:
        if args.record:
            record(robot)
        else:
            execute(robot)
    except KeyboardInterrupt:
        print("\nCtrl+C received.")
    finally:
        try:
            
            robot.move_j(HOME)
            time.sleep(3)
            
            print("Disabling robot...")
            robot.electronic_emergency_stop()
            print("Electronic emergency stop activated.")
            input()
            robot.reset()
            
        except Exception:
            pass
        time.sleep(0.3)
        print("Robot disabled. Bye.")


if __name__ == "__main__":
    main()
