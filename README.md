# 도심형 풀필먼트 물류 서비스: AMR 로봇 활용한 유통 대행 서비스
(기간: 2024년 07월 09일 ~ 2024년 08월 09일)
## 1. 👨‍🏫Project Introduction👨‍🏫
### 1-1. Project Purpose
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/588414cf-cd6e-493a-8922-550cee1ed006" width ="800">
  </div>

### 1-2. Technology Stack
  <div align=center>
      
   |**Category**|**Details**|
  |:----------:|:----------:|
  |**DEV**|<img src="https://img.shields.io/badge/Ubuntu22.04-E95420?style=for-the-badge&logo=Ubuntu22.04&logoColor=white"> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white"> |
  |**TECH**|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white"> <img src="https://img.shields.io/badge/ROS2-22314E?style=for-the-badge&logo=ros&logoColor=white"> <img src="https://img.shields.io/badge/YOLO-512BD4?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=Qt&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">|
  |**HW**|<img src="https://img.shields.io/badge/Rasberrypi4-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white">  <img src="https://img.shields.io/badge/Arduino-00878F?style=for-the-badge&logo=Arduino&logoColor=white"> <img src="https://img.shields.io/badge/ESP32-4285F4?style=for-the-badge&logoColor=white">|
  |**TOOL**|<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white"> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"> <img src="https://img.shields.io/badge/Confluence-172B4D?style=for-the-badge&logo=Confluence&logoColor=white"> <br> <img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white"> <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white"> <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=Figma&logoColor=white"> |
</div> 

### 1-3. Member Role
  <div align=center> 
  
|**구분**|**이름**|**역할**|
|:------:|:------:|:-------|
|팀장|채희곤|<ul><li> 메인 서버와 로봇, Arduino 보드 등 ROS 통신 제어</li> <li> 로봇 관제 시스템 통합 및 제어</li> <li> 로봇 관제 시스템 GUI 구현</li></ul>|
|팀원|김민경|<ul><li> 다중 로봇 작업 스케쥴링 알고리즘 구현</li> <li> Arduino 및 ESP32 보드 제어</li></ul>|
|팀원|손영수|<ul><li> 주행 경로 탐색 알고리즘 구현 </li> <li> 자율주행 로봇 환경 구축 </li></ul>|
|팀원|곽민기|<ul><li> 딥러닝 모델 학습 </li> <li> 주행 경로 탐색 알고리즘 구현 </li> <li> 주문 정보 시스템 GUI 구현</li></ul>|
</div> 

## 2. 👨🏻‍💻Project Design👨🏻‍💻
### 2-1. Main Process Flow Chart
#### 가정: MFC 내 작업장에서의 입/출고
* Inbound Flow
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/51fe083a-c311-44fb-98dc-525938d2381b" width ="800">
  </div>
  
* Outbound Flow
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/84abaf8a-6374-41bb-98e3-3bb80e60608e" width ="800">
  </div>

### 2-2. HW Architecture
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/bbe210e2-0043-4bbd-bae2-b25e9fa923a0" width ="800">
  </div>

### 2-3. System Architecture
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/f295b644-96dd-48dc-933a-1d3606856e08" height ="600">
  </div>

### 2-4. State Display
* Robot State
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/d6ae5b7c-06d1-4d36-a3c0-c716f89f2995" height ="400">
  </div>
* Items State in Rack 
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/e9c21807-a186-403f-b0ff-69f3bae9a9f4" height ="400">
  </div>
  
## 3. :star:Main Technology:star:
### 3-1. Multi-Robot Task Scheduling Algorithm ℹ️
#### 3-1-1. Order List Grouping
* **동일한 or 인접한** 렉에 물품들 Rack List로 그룹핑
* **Task Code(ex.Task1,2)** 로 Rack List를 관리하며 작업 할당 경매
    <div align=center> 
      <img src="https://github.com/user-attachments/assets/c86076f8-c001-46dc-8233-65be5feb02a0" width ="600">
  </div>

#### 3-1-2. Low-Cost Based Auction
* Task Code에 대한 **할당 비용이 가장 낮은 로봇 순**으로 작업 할당
* **3가지 변수**에 대한 모든 경우의 수 고려한 최적 비용값 설정
  * 1) **로봇 초기 상태**
  * 2) **충전 상태**
  * 3) **잔여 작업수**
       
  <div align=center> 
      <img src="https://github.com/user-attachments/assets/2153a576-e220-46d2-91f8-42c6dbec5270" width ="600">
  </div>
  
### 3-2. Path Planning ℹ️
#### A* Algorithm
* 1개 경로 당 **2개의 waypoint**들 생성
* 예측 가능한 waypoint 위주로 구성된 경로를 통해 돌발 상황 감소
  <div align=center>
  </br>
      <img src="https://github.com/user-attachments/assets/76bbd056-3494-42ba-aac9-706558c72fd1" width ="800">
      <img src="https://github.com/user-attachments/assets/d7e35464-f613-49b8-bd1d-34fecd68f8d7" width ="1000">
  </div>

### 3-3. DeepLearning ℹ️
#### Human Detection
* YOLOv5 Classification 모델 사용
* 주행 중 작업자 인식 시 우선 멈춤 동작
    <div align=center>
  </br>
      <img src="https://github.com/user-attachments/assets/96a3942c-b31e-4632-b888-fdefb94ccbba" width ="600">
      <img src="https://github.com/user-attachments/assets/3125f762-b074-413f-a7e1-384310f50d5c" width ="900">
  </div>

### 3-4. Order Information and Robot Control Management System ℹ️
* GUI 구현 화면
  <div align=center> 
      <br/>
      <img src="https://github.com/user-attachments/assets/6319ac9c-76ae-4877-9a7f-19c5a789b968" width ="800">
  </div>
* 입고 시나리오 _ 적재 시연 영상
  <div align=center> 
      <br/>
      <img src="https://github.com/user-attachments/assets/eec29ead-03fe-4bef-ac66-9cf52b09d7df" width ="600">
  </div>

## 4.  :exclamation:Prerequisite & Installation:exclamation:
### :warning:빌드시 주의사항:warning:
0. humble (ROS 환경 불러오기)
1. Local로 clone or pull했을 때, log, install, build 삭제 src파일만 남기기
2. workspace에서 의존성 자동 설치
    ```
    rosdep install --from-paths src --ignore-src -r -y
    ```
3. colcon build
### :warning:Docker에서 Ultralytics YOLO 모델 환경 구축하기:warning:
1. NVIDIA Docker 런타임을 설치하여 Docker 컨테이너에서 GPU 지원을 활성화
   ```
    # Add NVIDIA package repositories
    $ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
       && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
       && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    # Install NVIDIA Docker runtime
    $ sudo apt-get update
    $ sudo apt-get install -y nvidia-docker2

    # Restart Docker service to apply changes
    $ sudo systemctl restart docker
    ```
2. Docker 명령어로 NVIDIA 확인
    ```
    $ docker info | grep -i runtime
    ```
3. 작성된 Dockerfile을 사용해 Docker 이미지를 빌드.
    ```
    # 터미널을 열고 Dockerfile이 있는 디렉토리로 이동.
    cd docker

    # Docker 이미지를 빌드
    docker build -t my_ros2_yolov5:latest .
    ```
4. Docker 컨테이너 X 서버에 접근
   ```
   xhost +local:docker
   ```
5. Docker 컨테이너에서 Ultralytics 실행
    ```
    docker run --gpus all --network host \
    -v /ros-repo-4/AI_Server/src/ai_server/:/ros2_ws/src/ai_server \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=:0 \
    -e ROS_DISTRO=humble \
    -it my_ros2_yolov5:latest /bin/bash
    ```
### :warning:AWS RDS 상 DB 정보 로컬에 저장:warning:
0. AWS RDS 상 데이터베이스 백업
    ```
    ~/dev_ws/git_ws$ mysqldump -h database-1.cdigc6umyoh0.ap-northeast-2.rds.amazonaws.com -P 3306 -u root -p DFC_system_db > DFC_system_db.sql
    Enter password: AWS RDS PW
    ```
1. 로컬 디렉토리에 해당하는 sql 파일 로컬 MYSQL에 import
    ```
    ~/dev_ws/git_ws$ mysql -u root -p
    Enter password: 본인 로컬 MYSQL PW
    ```
    ```
    mysql > create database DFC_system_db;
    mysql > use DFC_system_db;
    mysql > SOURCE 'DFC_system_db.sql 위치한 절대 경로';
    mysql > show tables;
    ```

## 5. :white_check_mark:Usage:white_check_mark:
### 입고 시나리오 진행 순서
0. 파라미터 및 경로 설정하기
    ```
    # params/db_user_info.yaml
    local_db:
      id: "root"
      pw: "본인 로컬 MySQL 비밀번호"
    
    # ~/main_control_server/src/robot_state/src/robot_state_manager_node.py
    ## YAML 파일 경로
    yaml_file_path = '본인 PC db_user_info.yaml 절대 경로'
    
    ## YAML 파일을 읽어 파라미터를 가져옴
    def load_db_params(file_path):
        with open(file_path, 'r') as file:
            params = yaml.safe_load(file)
        return params['local_db']['id'], params['local_db']['pw']
    
    def get_mysql_connection():
        try:
            db_id, db_pw = load_db_params(yaml_file_path)
            db_instance = Connect(db_id, db_pw)
            return db_instance
        except con.Error as err:
            print(f"Error: {err}")
            return None    
    ```

1. esp32_master.ino 및 arduino_slave_1.ino 빌드하기
    ```
    # esp32_mater.ino
    const char* ssid = "와이파이 이름";
    const char* password = "비밀번호";
    
    String MFCNetworkManagerIP = "PC IP 주소"; // network_manager IP 주소. ifconfig로 확인하기
    
    # Serial Monitor
    ...
    11:16:43.140 -> IP address: 'ESP32 IP 주소'
    ...
    
    ```

2. communication_MFC_arduino.py 수정
    ```
    # ros-repo-4/main_control_server/src/network_manager/src/communication_MFC_arduino.py
    ...
    self.esp32_master = ESP32Master('ESP32 IP 주소', 80) # 시리얼 통신 클래스 인스턴스 생성
    ...
    
    def receive_inspection_server(self):
            self.check_and_close_existing_socket('PC IP 주소', 12345)
            ...
            receive_inspection_server_socket.bind(('PC IP 주소', 12345))  # 서버 IP와 포트 설정 ifconfig로 확인하기
            ...
    ```
    
3. 메인서버 내 노드 순차적 실행
    ```
    # 빌드 및 ros 환경 불러온 후
    ## 터미널 1
    ros2 run task_manager task_manager_node.py 
    
    ## 터미널 2
    ros2 run task_allocator task_allocator_node.py
    
    ## 터미널 3
    ros2 run robot_state robot_state_manager_node.py 
    
    ## 터미널 4(예시)
    ros2 topic pub /goal_status robot_state/msg/GoalStatus "{current_rack: 'R_D1', status: 'completed'}"
    
    ## 터미널 5
    ros2 run network_manager communication_MFC_arduino.py
    
    ## 터미널 6
    ros2 run main_server_gui main_server_gui.py 
    ```

4. GUI 상에서 START 8:00 AM 여러번 실행
* **아래 결과 나와야 액션 통신 준비 완료**
    ```
    ## 터미널 3
    ~$ ros2 run robot_state robot_state_manager_node.py 
    Update 전 초기값
    Debugging ['Debugging', 'Debugging', 'Debugging'] Debugging
    ################################################################
    [INFO] [1722479547.594396443] [mfc_robot_manager]: Received task assignment for robot: Robo1
    [INFO] [1722479547.594757637] [mfc_robot_manager]: Task Code: Task_1
    [INFO] [1722479547.594980065] [mfc_robot_manager]: Rack List: ['R_F3']
    [INFO] [1722479547.595161416] [mfc_robot_manager]: Task Assignment: 입고
    It is in MFCRobotManager
    Robo1 Task_1 ['R_F3'] 입고
    ################################################################
    Update 후
    Robo1 Task_1 ['R_F3'] 입고
    ################################################################
    [INFO] [1722479547.690252849] [robot_task_client]: Goal accepted: )
    ```
    ```
    ## 터미널 4
    ~$ ros2 topic pub /goal_status robot_state/msg/GoalStatus "{current_rack: 'R_D1', status: 'completed'}"
    ```
    
### 로봇 기동 순서 
0. 로봇에 원격 접속
  ```
  cd ~/final_project/ros-repo-4/scripts
  chmod +x launch_robot.sh launch_map.sh robot_drive.sh
  ```

1. 로봇 기동
  ```
  cd ~/final_project/ros-repo-4/scripts
  ./launch_robot.sh
  ```

2. (다른 터미널 열고) 내 PC에 있는 레파지토리에서 Path_server 코드 실행
  ```
  humble
  export ROS_DOMAIN_ID=48

  # MFC_Robot, main_control_server 모두 source install/local_setup.bash 해주기

  cd ~/final_project/ros-repo-4/main_control_server/
  source install/local_setup.bash

  cd ~/final_project/ros-repo-4/MFC_Robot/
  source install/local_setup.bash

  ros2 launch lrobot path_server_launch.py
  ```

3. (다른 터미널 열고) robot_drive 노드 실행
  ```
  cd ~/final_project/ros-repo-4/scripts
  ./robot_drive.sh
  ```

4. (다른 터미널 열고) nav2 맵 실행
  ```
  cd ~/final_project/ros-repo-4/scripts
  ./launch_map.sh
  ```

5. (다른 터미널 열고) 내 PC에 연결된 터미널에서 [임시] 목표 좌표 발행
  ```
  humble
  export ROS_DOMAIN_ID=48
  ros2 topic pub /target_pose minibot_interfaces/GoalPose "{position_x: 1.04, position_y: 1.45, orientation_z: 0.7, orientation_w: 0.7}" --once
  ```
### AI Server(docker)
1. docker 접속(새로운 pc에서 실행 권장)
 ```
  docker run --gpus all --network host \
  -v /ros-repo-4/AI_Server/src/ai_server/:/ros2_ws/src/ai_server \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=:0 \
  -e ROS_DISTRO=humble \
  -it my_ros2_yolov5:latest /bin/bash
 ```
2. 빌드
```
 ## 워크스페이스로 이동
 cd ../ros2_ws
 ```
   
 ```
 ## 빌드
 colcon build
 source install/local_setup.bash
 ```
   
 ```
 ## 서버 도메인 설정
 export ROS_DOMAIN_ID= ??
 ```
   
3. 실행
 ```
 ros2 run ai_server ai_sever
 ```
### Domain bridge
 ```
 # 빌드 
 cd ros-repo-4/main_control_server
 colcon build
 source install/local_setup.bash
 ```
 ```
 # 실행(실행하는 터미널의 도메인ID 상관X)
 cd config
 ros2 run domain_bridge domain_bridge bridge_config.yaml
 ```


