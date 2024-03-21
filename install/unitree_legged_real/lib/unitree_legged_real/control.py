#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros2_unitree_legged_msgs.msg import LowCmd
from ros2_unitree_legged_msgs.msg import HighCmd
from ros2_unitree_legged_msgs.msg import HighState
from ros2_unitree_legged_msgs.msg import BmsCmd
from ros2_unitree_legged_msgs.msg import BmsState
from ros2_unitree_legged_msgs.msg import Cartesian
from ros2_unitree_legged_msgs.msg import LowState
from ros2_unitree_legged_msgs.msg import MotorState
from ros2_unitree_legged_msgs.msg import MotorCmd
import time
"주요 로봇 제어 관련 항목은 중 위치는 position[3] 이며 [0]~[2]까지 각 x,y,z를 의미함"
"velocity[3]의 경우 로봇의 속도를 의미하며 [0]~[2]는 각 직전속도, 좌우로 이동할 때 속도, 상하(눕거나, 일어서거나 뭐.. 그런거) 속도를 의미함 "


class Control(Node):
    def __init__(self):
        super().__init__('my_node')
        self.pub = self.create_publisher(HighCmd,"high_cmd",10)
        self.count=0

    def create_msg(self):
        self.high_cmd_ros = HighCmd()
        self.high_cmd_ros.head[0] = 0xFE
        self.high_cmd_ros.head[1] = 0xEF
        self.high_cmd_ros.level_flag = 0x00
        self.high_cmd_ros.mode = 0
        self.high_cmd_ros.gait_type = 0
        self.high_cmd_ros.speed_level = 0
        self.high_cmd_ros.foot_raise_height = 0.0
        self.high_cmd_ros.body_height = 0.0
        self.high_cmd_ros.euler[0] = 0
        self.high_cmd_ros.euler[1] = 0
        self.high_cmd_ros.euler[2] = 0
        self.high_cmd_ros.velocity[0] = 0.0
        self.high_cmd_ros.velocity[1] = 0.0
        self.high_cmd_ros.yaw_speed = 0.0
        self.high_cmd_ros.reserve = 0

    def control_cmd(self):
        while self.count < 2000:
            self.count += 2
            if self.count < 2000:
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 1.0
                self.high_cmd_ros.velocity[1] = -1.0 #양수는 왼쪽
                self.pub.publish(self.high_cmd_ros)
        print("보냄")


def main(args=None):
    rclpy.init(args=args)
    node = Control()
    node.create_msg()
    node.control_cmd()
    print("end")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
























