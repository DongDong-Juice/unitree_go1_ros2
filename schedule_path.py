#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ros2_unitree_legged_msgs.msg import HighCmd
from geometry_msgs.msg import PoseStamped ,Pose
import sys, select, termios, tty, time , math, schedule, json, re
import numpy as np
settings = termios.tcgetattr(sys.stdin)


class Schedule(Node):
    def __init__(self):
        super().__init__('Schedule')
        self.pub = self.create_publisher(HighCmd, "high_cmd", 10)
        self.radian = 0.0174533  # 각도를 라디안으로 바꾸기 위한 상수 값
        self.path_list = np.empty(shape=4)  # 경로 정보를 담을 numpy 배열 초기화
        print("스케줄링 모드 시작")
        try:
            print("몇 번째 경로를 예약 하시겠습니까?")
            selet_path = self.getKey()
            self.schedule_reservation(selet_path)
        except Exception as e:
            print(f"error: {e}")

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

    def schedule_reservation(self, selet_path: str = "1"):
        print("입력 순서: 주간 일일 시간 분 초 (예약하지 않는 항목은 0 입력 및 각 항목 별 띄어 쓰기로 구분) : ")
        user_input = input()
        integers = re.findall(r'\d+', user_input)
        print("입력한 문자열에서 추출된 정수 부분:", integers)
        if integers[0] != "0":
            schedule.every(int(integers[0])).week.do(self.open_path_file, selet_path)
        elif integers[1] != "0":
            schedule.every(int(integers[1])).day.do(self.open_path_file, selet_path)
        elif integers[2] != "0":
            schedule.every(int(integers[2])).hours.do(self.open_path_file, selet_path)
        elif integers[3] != "0":
            schedule.every(int(integers[3])).minutes.do(self.open_path_file, selet_path)
        elif integers[4] != "0":
            schedule.every(int(integers[4])).seconds.do(self.open_path_file, selet_path)
        else:
            self.open_path_file(selet_path)
        while 1:
            schedule.run_pending()
            time.sleep(1)

    def open_path_file(self, choose):
        if choose == "1":
            with open('/home/dong/ros2_ws/src/unitree_ros2_to_real/path/path1.json', 'r') as f:
                data = json.load(f)
                self.path_plan_data(data)
        elif choose == "2":
            with open('/home/dong/ros2_ws/src/unitree_ros2_to_real/path/path2.json', 'r') as f:
                data = json.load(f)
                self.path_plan_data(data)
        elif choose == "3":
            with open('/home/dong/ros2_ws/src/unitree_ros2_to_real/path/path3.json', 'r') as f:
                data = json.load(f)
                self.path_plan_data(data)
        else:
            print("잘못 선택 하셨습니다 ")

    def path_plan_data(self, data):  # datas
        index = [i['index'] for i in data]
        x = [i['x'] for i in data]
        y = [i['y'] for i in data]
        z = [i['z'] for i in data]
        w = [i['w'] for i in data]
        self.path_list = np.array([index, x, y, z, w])
        print("경로 ", self.path_list)
        self.path_plan()

    def path_plan(self):
        """
        self.path_list[0] = index
        self.path_list[1] = x
        self.path_list[2] = y
        self.path_list[3] = z
        self.path_list[4] = w
        해당 배열 항목 속 원소 접근은 ex) self.path_list[0][0] = index 항목에 0번째 원소
        """
        print("경로 출력 ",self.path_list[1][0])
        #현재 내 위치를 알수 있는 방법이 없어...잠정 중단


    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


def main(args=None):
    rclpy.init(args=args)
    node = Schedule()
    print("프로그램 종료: ctrl + c ")
    node.create_msg()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()