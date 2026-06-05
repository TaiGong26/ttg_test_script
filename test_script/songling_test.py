from pyAgxArm import create_agx_arm_config, AgxArmFactory
import time

robot_cfg = create_agx_arm_config(robot="nero", comm="can", channel="can0", interface="socketcan")
robot = AgxArmFactory.create_arm(robot_cfg)
robot.connect()
robot.set_normal_mode()
# if robot is None:
#     print("连接失败")
# print(f"robot{robot}")

# robot.disable()
while not robot.enable():
   time.sleep(0.1)
   print("waiting... enable robot")
time.sleep(1.5)


robot.set_speed_percent(80)
# robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
# time.sleep(0.5)
# robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
# time.sleep(0.5)
# robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
# time.sleep(0.5)

# # # robot.move_l([-0.4, -0.2, 0.4, 1.5708, 0.0, 0.0])

# # robot.move_j([0.40338049672092946, -0.9550965265688569, 0.9833010472810852, 1.2129340169659792, 1.835335881519677, -0.12925908440270006, -0.46739917368408146])

# # robot.move_j([1.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
# # time.sleep(0.3)
# # robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])

# start_pose = [-0.268651, 0.298402, 0.417091, -2.3193854962677842, 1.1728961639252293, -1.5040549361986335]
# mid_pose =  [0.07972599999999999, 0.374799, 0.428819, -3.124994572403327, 0.7780154206615123, -2.7185422961988874]
# end_pose =[0.220445, 0.24997599999999998, 0.484903, -3.082513258409785, 1.1412358912940523, 2.7885125459113405]
# # # time.sleep(0.5)
# # # while not robot.enable():
# # #     time.sleep(0.01)
time.sleep(1.5)
# robot.move_c(start_pose,mid_pose,end_pose)
# # time.sleep(0.5)
robot.move_p( [-0.158411, 0.253476, 0.358715, -2.990255154149365, 0.8693135938333356, -0.4432089102514401])
# robot.move_l( [-0.158411, 0.253476, 0.358715, -2.990255154149365, 0.8693135938333356, -0.4432089102514401])

# [-0.337707, 0.160734, 0.474134, 3.0306595263330336, 1.5164118673027533, 1.1979939985689079]
# # # # print(f"start_pose{start_pose} \n mid_pose{mid_pose} \n end_pose{end_pose}")
cnt=0
flag1=True
flag2=False
while True:
    try:
        # status = robot.get_arm_status()
        # if status is not None and status.msg.motion_status == 0:
        #     print("已到达目标位置")
        
        cnt +=1
        if cnt == 5:  # Stop after 10 seconds (assuming 100 iterations at 0.1s each)
            robot.move_l( [-0.337707, 0.160734, 0.474134, 3.0306595263330336, 1.5164118673027533, 1.1979939985689079])
            robot.move_p( [-0.158411, 0.253476, 0.358715, -2.990255154149365, 0.8693135938333356, -0.4432089102514401])
            print("=/======================================================== new line")
        # robot.move_c(start_pose,mid_pose,end_pose)

        
        # if cnt < 20:
        #     if flag1:
        #         robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
        #         flag1=False
        #         flag2=True
        #     # robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
        #     # time.sleep(2)
        # else:
        #     if flag2:
        #         robot.move_j([1.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
        #         flag2=False
        #         flag1=True
        #     # time.sleep(2)
            
        # cnt%=40
            
        # robot.move_j([2.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
        # time.sleep(0.5)
        # robot.move_j([1.027740978259532, -1.0642668712811023, 0.028850292535466268, 1.1100817641459535, 1.5530288750095944, -0.1593136541220424, -0.46743408026912137])
        # time.sleep(0.5)
        
        
        
        # flange = robot.get_flange_pose().timestamp
        print(robot.get_flange_pose())
        # t = time.time()
        # print(f"Flange Pose Timestamp: {flange}, Time: {t} Diff: {t - flange:.4f} seconds")
        
        # print(robot.get_arm_status())
        # print(robot.get_joint_angles())
        # robot.move_j([1.2427966004676023, -0.8054345432103432, 0.17526596348527057, 0.9321803534901715, -0.034714598822167216, -0.5935341187257116, 0.3521899897599358])
        # e = robot.get_joint_angles().msg
        # print()
        # s = [0.40338049672092946, -0.9550965265688569, 0.9833010472810852, 1.2129340169659792, 1.835335881519677, -0.12925908440270006, -0.46739917368408146]
        # robot.move_j(s)
        
        # # # print(e)
        # for status, cmd in zip(e, s):
        #     print(f"j:{status - cmd:.4f}", end=" ")
        # print()
        
        time.sleep(0.1)
        # cnt+=1
        # if cnt == 100:  # Stop after 10 seconds (assuming 100 iterations at 0.1s each)
            # robot.move_c(start_pose,mid_pose,end_pose)
            # print("=/======================================================== new circle")
        
    except KeyboardInterrupt as e:
        # print(f"start_pose{start_pose} \n mid_pose{mid_pose} \n end_pose{end_pose}")
        robot.disable()
        # robot.electronic_emergency_stop()
        time.sleep(2)
        print("==========================================================")
        break
    
