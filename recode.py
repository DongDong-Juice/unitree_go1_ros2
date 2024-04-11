#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros2_unitree_legged_msgs.msg import HighCmd
from geometry_msgs.msg import PoseStamped ,Pose
import sys, select, termios, tty, time , math, schedule_path, json, re
import numpy as np
"""주요 로봇 제어 관련 항목은 중 위치는 position[3] 이며 [0]~[2]까지 각 x,y,z를 의미함, 로봇의 현재 위치 같음 무쓸모
velocity[3]의 경우 로봇의 속도를 의미하며 [0]~[2]는 각 직전속도, 좌우로 이동할 때 속도, 상하(눕거나, 일어서거나 뭐.. 그런거) 속도를 의미함
velocity[0] 양수 = 로봇개 머리 기준 정면 음수 반대, velocity[1] = 양수 로봇개 머리 기준 왼쪽 음수 반대
 self.count += 2
    if self.count < 2000:

 """


"""
    def going_robot(self,meter):
        self.high_cmd_ros.mode = 2
        self.high_cmd_ros.yaw_speed = 0.0 #일 직선으로 전진을 위한 회전 0으로 초기화
        count = meter * 2
        for i in range(int(count)):
            self.high_cmd_ros.velocity[0] = 0.5
            self.pub.publish(self.high_cmd_ros)
            time.sleep(1)

    def turn_robot(self, angle: int = 0) -> float:
        #특정 각도 만큼 로봇을 회전하고 싶을때 사용
        #angle -> positive number = turn right
        #angle -> negative number = turn left
        self.high_cmd_ros.mode = 2
        self.high_cmd_ros.velocity[0] = 0.0
        if angle > 0:
            self.high_cmd_ros.yaw_speed = -angle * self.radian  # 각도를 라디안 값으로 바꾸는 공식
        if angle < 0:
            self.high_cmd_ros.yaw_speed = angle * self.radian  # 각도를 라디안 값으로 바꾸는 공식
        if angle == 0:
            self.high_cmd_ros.yaw_speed = 0.0
        self.pub.publish(self.high_cmd_ros)

    def global_path(self):
        PathCount = 0
        print("5초후 시작")
        while 1:
            if PathCount == 0:
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 1:
                self.turn_robot(45)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 2:
                self.turn_robot(45)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 3:
                self.turn_robot(-90)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 4:
                self.turn_robot(-90)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 5:
                self.turn_robot(-90)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 6:
                self.turn_robot(-45)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 7:
                self.turn_robot(-45)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            elif PathCount == 8:
                self.turn_robot(-90)
                self.going_robot(5)
                PathCount += 1
                time.sleep(2)
            else:
                break
"""
