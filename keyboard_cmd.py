#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ros2_unitree_legged_msgs.msg import HighCmd
import sys, select, termios, tty, time
settings = termios.tcgetattr(sys.stdin)


class Keyboard(Node):
    def __init__(self):
        super().__init__('my_node')
        self.radian = 0.0174533  # 각도를 라디안으로 바꾸기 위한 상수 값
        self.pub = self.create_publisher(HighCmd, "high_cmd", 10)

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

    def going_robot(self,meter: float = 0.5):
        self.high_cmd_ros.mode = 2
        self.high_cmd_ros.yaw_speed = 0.0 #일 직선으로 전진을 위한 회전 0으로 초기화
        count = meter * 2
        if meter > 0:
            for i in range(int(count)):
                self.high_cmd_ros.velocity[0] = 0.5
                self.pub.publish(self.high_cmd_ros)
                time.sleep(1)
        elif meter < 0:
            for i in range(int(count)):
                self.high_cmd_ros.velocity[0] = -0.5
                self.pub.publish(self.high_cmd_ros)
                time.sleep(1)

    def turn_robot(self, angle: int = 0) -> float:
        """
        특정 각도 만큼 로봇을 회전하고 싶을때 사용
        angle -> positive number = turn right
        angle -> negative number = turn left
        """
        self.high_cmd_ros.mode = 2
        self.high_cmd_ros.velocity[0] = 0.0
        if angle > 0:
            self.high_cmd_ros.yaw_speed = -angle * self.radian  # 각도를 라디안 값으로 바꾸는 공식
        if angle < 0:
            self.high_cmd_ros.yaw_speed = angle * self.radian  # 각도를 라디안 값으로 바꾸는 공식
        if angle == 0:
            self.high_cmd_ros.yaw_speed = 0.0
        self.pub.publish(self.high_cmd_ros)

    def control_key(self):
        while True:
            key = self.getKey()
            if key == 'w':
                self.going_robot(0.5)
                print("전진")
            elif key == 'a':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0.3  # 양수는 왼쪽
                print("왼쪽")
            elif key == 's':
                self.going_robot(-0.5)
                print("후진")
            elif key == 'd':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = -0.3
                print("오른쪽")
            elif key == 'l':
                self.turn_robot(10)
                print("오른쪽 회전")
            elif key == 'k':
                self.turn_robot(-10)
                print("왼쪽 회전")
            elif key == 'q':
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0
                self.high_cmd_ros.yaw_speed = 0.0
                print("종료")
                break
            else:
                self.high_cmd_ros.mode = 2
                self.high_cmd_ros.velocity[0] = 0
                self.high_cmd_ros.velocity[1] = 0
                self.high_cmd_ros.yaw_speed = 0.0
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
    node = Keyboard()
    print("프로그램 종료: ctrl + c ")
    node.create_msg()
    node.control_key()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('key end')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
