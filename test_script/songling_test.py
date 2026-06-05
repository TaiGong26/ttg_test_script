# from pyAgxArm import create_agx_arm_config, AgxArmFactory,ArmModel
# import time

# # robot_cfg = create_agx_arm_config(robot="piper", comm="can", channel="can_left", interface="socketcan")
# robot_cfg = create_agx_arm_config(robot=ArmModel.PIPER, comm="can", channel="can_left", interface="socketcan")

# robot = AgxArmFactory.create_arm(robot_cfg)
# robot.connect()
# # robot.set_motion_mode()
# # if robot is None:
# #     print("连接失败")
# # print(f"robot{robot}")

# # robot.disable()
# while not robot.enable():
#    time.sleep(0.1)
#    print("waiting... enable robot")
# time.sleep(1.5)


# while True:
#     try:
        
#         print(robot.get_joint_angles())
        
        
#         time.sleep(0.1)
        
#     except KeyboardInterrupt as e:
#         # print(f"start_pose{start_pose} \n mid_pose{mid_pose} \n end_pose{end_pose}")
#         robot.disable()
#         # robot.electronic_emergency_stop()
#         time.sleep(2)
#         print("==========================================================")
#         break
    

import time
from pyAgxArm import create_agx_arm_config, AgxArmFactory, ArmModel, PiperFW

cfg = create_agx_arm_config(robot=ArmModel.PIPER, firmeware_version=PiperFW.DEFAULT, channel="can0")
robot = AgxArmFactory.create_arm(cfg)
robot.connect()
robot.reset()
# robot.enable()

while True:
    ja = robot.get_joint_angles()
    if ja is not None:
        print(ja.msg)
        print(ja.hz, ja.timestamp)
    time.sleep(0.005)