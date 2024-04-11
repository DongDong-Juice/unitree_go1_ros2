#!/usr/bin/env python3
import subprocess
# 실행할 스크립트 파일 경로
keyboard_script_path = "/home/dong/ros2_ws/src/unitree_ros2_to_real/src/keyboard_cmd.py"
path_script_path = "/home/dong/ros2_ws/src/unitree_ros2_to_real/src/single_path_planning.py"
schedule_script_path = "/home/dong/ros2_ws/src/unitree_ros2_to_real/src/schedule_path.py"



while True:
    print("원하는 모드에 해당 되는 정수를 입력해 주세요")
    print("1. 키보드 제어 모드")
    print("2. 단일 경로 모드")
    print("3. 스케쥴링 모드")
    user_input = input()
    if user_input == "1":
        subprocess.run(args=[keyboard_script_path])
        break
    elif user_input == "2":
        subprocess.run(args=[path_script_path])
        break
    elif user_input == "3":
        subprocess.call(args=[schedule_script_path])
        break
    else:
        print("잘못 입력 하셨습니다 다시 입력 해주세요 ")