import rclpy
import threading
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Quaternion
from nav_msgs.msg import Path
from robot_state.msg import RackList, GoalStatus
from lrobot.a_star import AStarPlanner  # AStar 클래스 임포트
from std_msgs.msg import Bool


pose_dict = {
    "R_A1": [0.14, 1.50, 0.7, 0.7], "R_A2": [0.14, 1.50, 0.7, 0.7], "R_A3": [0.14, 1.50, 0.7, 0.7],
    "R_B1": [0.72, 1.50, 0.7, 0.7], "R_B2": [0.72, 1.50, 0.7, 0.7], "R_B3": [0.72, 1.50, 0.7, 0.7],
    "R_C1": [1.05, 1.50, 0.7, 0.7], "R_C2": [1.05, 1.50, 0.7, 0.7], "R_C3": [1.05, 1.50, 0.7, 0.7],
    "R_D1": [0.16, 0.45, 0.7, 0.7], "R_D2": [0.16, 0.45, 0.7, 0.7], "R_D3": [0.16, 0.45, 0.7, 0.7],
    "R_E1": [0.72, 0.45, 0.7, 0.7], "R_E2": [0.72, 0.45, 0.7, 0.7], "R_E3": [0.72, 0.45, 0.7, 0.7],
    "R_F1": [1.08, 0.45, 0.7, 0.7], "R_F2": [1.08, 0.45, 0.7, 0.7], "R_F3": [1.08, 0.45, 0.7, 0.7],
    "IB": [0.42, -0.80, -0.7, 0.6], "OB": [0.85, -0.80, -0.7, 0.6], 
    "R1": [0.0, 0.0, 0.0, 1.0], # "R2": [0.0, 0.3, 0.0, 1.0],
}


class PathServer(Node):
    def __init__(self):
        super().__init__('path_server1')

        self.initial_position = (0.0, 0.0)
        self.current_pose = None
        self.goal_pose = None
        self.path_index = 0  # 현재 목표 인덱스
        self.goal_list = []
        self.light_off_2 = False
        self.go_home_2 = False
        self.arrived = False
        
        self.lock = threading.Lock()
        
        # Subscriber
        self.pose_subscription = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10)
        self.rack_list_subscription = self.create_subscription(RackList, 'rack_list_1', self.goal_callback, 10)
        self.task_done_subscription = self.create_subscription(Bool, 'light_off_1', self.light_on_callback2, 10)
        self.arrive_subscription = self.create_subscription(Bool, 'Arrive', self.arrive_callback, 10)
        # self.go_home_subscription = self.create_subscription(Bool, 'go_home_2', self.go_home_callback, 10)
        # self.battery_home_subscription = self.create_subscription(mya, 'battery_home_2', self.battery_home_callback2, 10)
        
        # Publisher
        self.path_publisher_2 = self.create_publisher(Path, 'planned_path_2', 10)
        self.arrive__send_publisher_2 = self.create_publisher(GoalStatus, 'goal_status', 10)

        # self.timer = self.create_timer(3.0, self.timer_callback)  # 3초마다 timer_callback 실행
        # self.timer.cancel()  # 타이머를 초기에는 비활성화

        self.path_thread = threading.Thread(target=self.path_processing_thread)
        self.path_thread.start()
        
    def pose_callback(self, msg):
        self.current_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y)
        self.get_logger().info(f'Current pose: {self.current_pose}')
    
    def light_on_callback2(self, msg: Bool):
        if msg.data:
            with self.lock:
                self.light_off_2 = True
            self.get_logger().info("Rack List 내 직전 goal location LED 켜졌다. 다음 goal location으로 이동해야함")
            self.process_next_goal()  # 다음 목표로 이동
    
    # def battery_home_callback2(self, msg):
    #     if msg.data == 'R1':  # 배터리 토픽을 통해 집으로 가라고 하면
    #         self.get_logger().info("Returning to home position R1")
    #         # R1에 해당하는 좌표를 목표로 설정
    #         home_pose = pose_dict.get('R1', None)
    #         if home_pose:
    #             with self.lock:
    #                 self.goal_pose = home_pose
    #                 self.move_to_target()  # 목표로 이동         
    
    def arrive_callback(self, msg: Bool):
        if msg.data:
            goal_status_msg = GoalStatus()
            with self.lock:
                goal_status_msg.current_rack = self.goal_list[self.path_index - 1]
            goal_status_msg.status = 'completed'
            self.arrive__send_publisher_2.publish(goal_status_msg)
            self.get_logger().info(f"Published Goal Status: {goal_status_msg.current_rack}, {goal_status_msg.status}")
    
    
    # 렉 리스트 수신
    def goal_callback(self, msg):
        with self.lock:
            self.goal_list = msg.rack_list
            
            # scenario가 True이면 rack_list의 마지막 인덱스에 "OB" 추가
            if msg.scenario:
                self.goal_list.append("OB")
                self.light_off_2 = True
            # scenario가 False이면 rack_list의 첫 번째 인덱스에 "IB" 추가
            else:
                self.goal_list.insert(0, "IB")
                self.light_off_2 = False

            if len(self.goal_list) == 0:
                self.get_logger().info("Received empty goal list.")
                return

            self.path_index = 0
            self.get_logger().info(f'Received new rack list: {self.goal_list}')
            self.process_next_goal()  # 다음 목표로 이동
            print(1)

    def path_processing_thread(self):
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
    
    def process_next_goal(self):
        print(0)
      
        if not self.goal_list:
            self.get_logger().info("No goals to process.")
            return
        print(2)
        if self.current_pose and self.path_index < len(self.goal_list):
            key = self.goal_list[self.path_index]
            self.goal_pose = pose_dict.get(key, None)
            if self.goal_pose:
                self.light_off_2 = False
                self.move_to_target()
                print(3)
            else:
                self.get_logger().error(f"Invalid goal key: {key}")
        elif self.path_index >= len(self.goal_list):
            print(4)
            self.get_logger().info("All goals processed.")
            self.light_off_2 = False  # 모든 목표를 완료했으므로 플래그 초기화
            if len(self.goal_list) == 0:
                self.go_home_2 = True
                self.light_off_2 = True  # R1 복귀 대기 상태로 설정
                # self.timer.reset()  # 타이머 시작

    def move_to_target(self):
        print(5)
        if not self.goal_pose:
            self.get_logger().error("Goal pose is not set.")
            return
        print(6)
        sx_real, sy_real = self.current_pose if self.current_pose else self.initial_position
        gx_real, gy_real, gz_real, gw_real = self.goal_pose

        sx_real = round(sx_real, 2)
        sy_real = round(sy_real, 2)
        gx_real = round(gx_real, 2)
        gy_real = round(gy_real, 2)

        # A* 경로 계획 수행
        a_star = AStarPlanner(resolution=1, rr=0.4, padding=1)
        
        rx, ry, tpx, tpy, tvec_x, tvec_y = a_star.planning(sx_real, sy_real, gx_real, gy_real)

        if not tpx or not tpy:
            self.get_logger().error("No path found")
            return
 
        path = Path()
        path.header.frame_id = 'map'
        path.header.stamp = self.get_clock().now().to_msg()  
        print(7)
        for x, y in zip(tpx, tpy):
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation = Quaternion(z=gz_real, w=gw_real)
            path.poses.append(pose)

        
        self.path_publisher_2.publish(path)
        self.get_logger().info(f"Published path with {len(tpx)} waypoints.")
        print(8)
        self.path_index += 1  # 다음 목표로 인덱스 증가
        
    # def timer_callback(self):
    #     # 3초 후 R1으로 이동
    #     if self.go_home_2:
    #         self.get_logger().info("3 seconds elapsed. Returning to home position R1.")
    #         home_pose = pose_dict.get('R1', None)
    #         if home_pose:
    #             with self.lock:
    #                 self.goal_pose = home_pose
    #                 self.move_to_target()  # 목표로 이동
    #         self.go_home_2 = False  # 복귀 동작 완료, 상태 초기화
    #         self.timer.cancel()  # 타이머 비활성화

def main(args=None):
    rclpy.init(args=args)
    path_server = PathServer()
    try:
        rclpy.spin(path_server)
    except KeyboardInterrupt:
        pass
    finally:
        path_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()