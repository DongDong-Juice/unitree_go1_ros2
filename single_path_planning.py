#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros2_unitree_legged_msgs.msg import HighCmd
from geometry_msgs.msg import PoseStamped ,Pose
import sys, select, termios, tty, time , math, schedule, json, re
import numpy as np
"""주요 로봇 제어 관련 항목은 중 위치는 position[3] 이며 [0]~[2]까지 각 x,y,z를 의미함, 로봇의 현재 위치 같음 무쓸모
velocity[3]의 경우 로봇의 속도를 의미하며 [0]~[2]는 각 직전속도, 좌우로 이동할 때 속도, 상하(눕거나, 일어서거나 뭐.. 그런거) 속도를 의미함
velocity[0] 양수 = 로봇개 머리 기준 정면 음수 반대, velocity[1] = 양수 로봇개 머리 기준 왼쪽 음수 반대
 self.count += 2
    if self.count < 2000:

 """

settings = termios.tcgetattr(sys.stdin)


class Single_path_planning(Node):
    def __init__(self):
        super().__init__('my_node')
        self.pub = self.create_publisher(HighCmd,"high_cmd",10)
        self.sub = self.create_subscription(PoseStamped, "/goal_pose", self.path_plan, 1)
        self.radian = 0.0174533 #각도를 라디안으로 바꾸기 위한 상수 값
        self.path_list = np.empty(shape=4) # 경로 정보를 담을 numpy 배열 초기화

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

    def get_angle(self, x: float = 0, y: float = 0, x1: float = 0, y1: float = 0) -> float:
        """
        input
        x = 현재 로봇의 x 좌표
        y = 현재 로봇의 y 좌표
        x1 = 현재 로봇의 다음 목표 x 좌표
        y2 = 현재 로봇의 다음 목표 y 좌표
        out put
        angle(ridian) = 회전각도
        """
        angle = math.atan2(y1 - y, x1 - x)
        return angle

    def path_plan(self,msg):
        #imu가 없어서 불안정한 로직 추후 imu 있는 lidar 달리면 수정 24.4.1
        self.create_msg()
        self.high_cmd_ros.speed_level = 0
        self.high_cmd_ros.mode = 2
        self.speed = msg.pose.position.x
        self.high_cmd_ros.yaw_speed = self.get_angle(msg.pose.position.x, msg.pose.position.y)
        print("회전: ",self.high_cmd_ros.yaw_speed)
        self.pub.publish(self.high_cmd_ros)
        time.sleep(2)
        self.high_cmd_ros.yaw_speed = 0.0
        ab = int(float(self.speed)/ 0.5)
        for i in range(ab):
            self.high_cmd_ros.velocity[0] = 0.5
            self.pub.publish(self.high_cmd_ros)
            time.sleep(1)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


def main(args=None):
    rclpy.init(args=args)
    node = Single_path_planning()
    #print("모드 재선택 q ")
    print("프로그램 종료: ctrl + c ")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
