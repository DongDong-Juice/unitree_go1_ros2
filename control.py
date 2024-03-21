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
import sys, select, termios, tty
"""주요 로봇 제어 관련 항목은 중 위치는 position[3] 이며 [0]~[2]까지 각 x,y,z를 의미함, 로봇의 현재 위치 같음 무쓸모
velocity[3]의 경우 로봇의 속도를 의미하며 [0]~[2]는 각 직전속도, 좌우로 이동할 때 속도, 상하(눕거나, 일어서거나 뭐.. 그런거) 속도를 의미함
velocity[0] 양수 = 로봇개 머리 기준 정면 음수 반대, velocity[1] = 양수 로봇개 머리 기준 왼쪽 음수 반대
 self.count += 2
    if self.count < 2000:

 """

settings = termios.tcgetattr(sys.stdin)


class Control(Node):
    def __init__(self):
        super().__init__('my_node')
        self.pub = self.create_publisher(HighCmd,"high_cmd",10)
        self.angle =0

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
        while 1:
            self.high_cmd_ros.speed_level = 0
            self.high_cmd_ros.yaw_speed = 0.0
            self.high_cmd_ros.velocity[0] = 0.0
            self.high_cmd_ros.velocity[1] = 0.0

            key = self.getKey()
            if key == 'w':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0.3
                print("전진")
            elif key == 'a':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0.3  # 양수는 왼쪽
                print("왼쪽")
            elif key == 's':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = -0.3
                print("후진")
            elif key == 'd':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = -0.3
                print("오른쪽")
            elif key == 'l':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.yaw_speed = -0.5
                print("오른쪽 회전")
            elif key == 'k':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.yaw_speed = 0.5
                print("왼쪽 회전")
            elif key == 'q':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0
                print("종료")
                break
            else:
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0
                print("조작: wasd , 종료 q ")
            print(f"현재 모드: {self.high_cmd_ros.mode}, 현재 velocity: {self.high_cmd_ros.velocity}, 현재 euler: {self.high_cmd_ros.euler}")
            self.pub.publish(self.high_cmd_ros)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


def main(args=None):
    rclpy.init(args=args)
    node = Control()
    node.create_msg()
    node.control_cmd()
    print("end: ctrl + c ")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
























