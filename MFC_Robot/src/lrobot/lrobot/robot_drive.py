import rclpy
import math
import time
import threading
from enum import Enum
from rclpy.node import Node
from nav_msgs.msg import Path
from nav_msgs.msg import Path
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, Twist
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String, Bool
from collections import deque
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, QoSHistoryPolicy

class RobotState(Enum):
    STOP = 1
    MOVING = 2
    ADJUSTING = 3
    ARRIVED = 4
    GO_HOME = 5
    AT_HOME = 6
    # OBSTACLE = 7
    # TASK_DONE = 8


class PathFollower(Node):
    def __init__(self):
        super().__init__('mfc_robot')

        # QoS 설정
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE
        )
        
        self.subscription = self.create_subscription(Path, 'planned_path_2', self.path_callback, 10)
        self.amcl_subscription = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.amcl_callback, 10)
        # self.adjustment_complete_subscription = self.create_subscription(String, 'robo_2/adjust_complete', self.adjustment_complete_callback, 10)
        self.laser_subscription = self.create_subscription(LaserScan, 'scan', self.laser_callback, qos_profile)
        
        self.initial_pose_publisher = self.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)
        self.arrive_publisher = self.create_publisher(Bool, "Arrive", 10) 
        # self.battery_publisher = self.create_publisher(String, 'left_battery_2', 10)
        self.robot_state_publisher = self.create_publisher(String, 'robo_2/robot_state', 10) 
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        self.nav = BasicNavigator()
        self.nav.waitUntilNav2Active()

        self.publish_initial_pose()

        self.current_position = None
        self.current_orientation = None
        self.path_following_thread = None
        self.state_changed = False
        self.arrived = False
        self.obstacle_detected = False
        self.state = RobotState.STOP
        
        self.lock = threading.Lock()

        self.front_angle_range = 15

    def set_state(self, new_state):
        with self.lock:
            if self.state != new_state:
                self.state = new_state
                self.publish_status()

    def publish_status(self):
        robot_state_msg = String()
        robot_state_msg.data = self.state.name 
        self.robot_state_publisher.publish(robot_state_msg)
        self.get_logger().info(f"Published state: {self.state.name}")

    # def battery_home(self, msg):
    #     # Check if the last waypoint is (0,0)
    #     if self.last_waypoint_is_home:
    #         self.set_state(RobotState.GO_HOME)
    #         self.get_logger().info("Going Home")
    #         # Follow the path to go home
    #         self.follow_path(self.current_path_poses)
    #     else:
    #         self.get_logger().warn("Battery signal received, but last waypoint is not home.")


    def publish_initial_pose(self):
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.frame_id = 'map'
        pose_msg.header.stamp = self.get_clock().now().to_msg()


        pose_msg.pose.pose.position.x = 0.0
        pose_msg.pose.pose.position.y = 0.0
        pose_msg.pose.pose.position.z = 0.0
        pose_msg.pose.pose.orientation.x = 0.0
        pose_msg.pose.pose.orientation.y = 0.0
        pose_msg.pose.pose.orientation.z = 0.0
        pose_msg.pose.pose.orientation.w = 1.0


        pose_msg.pose.covariance = [0.0] * 36


        self.initial_pose_publisher.publish(pose_msg)
        self.get_logger().info("Published initial pose")

    def amcl_callback(self, msg):
        with self.lock: 
            self.current_position = msg.pose.pose.position
            self.current_orientation = msg.pose.pose.orientation

    def laser_callback(self, msg):
        angle_increment = msg.angle_increment 
        num_angles = len(msg.ranges) 
        mid_index = num_angles // 2 
        half_front_range = int((self.front_angle_range / 360) * num_angles / 2)

        front_distances = msg.ranges[mid_index - half_front_range: mid_index + half_front_range]

        min_distance = 0.05
        self.obstacle_detected = any(distance < min_distance for distance in front_distances)
        if self.obstacle_detected:
            # self.get_logger().warn("Obstacle detected in front! Stopping robot.")
            self.stop_robot()
            # self.set_state(RobotState.OBSTACLE)

    # def laser_callback(self, msg):
    #     if self.state != (RobotState.ARRIVED or RobotState.STOP):
    #         angle_increment = msg.angle_increment 
    #         num_angles = len(msg.ranges) 
    #         mid_index = num_angles // 2 
    #         half_front_range = int((self.front_angle_range / 360) * num_angles / 2)

    #         front_distances = msg.ranges[mid_index - half_front_range: mid_index + half_front_range]

    #         min_distance = 0.05  # 장애물 회피 임계 거리
    #         self.obstacle_detected = any(distance < min_distance for distance in front_distances)
            
    #         if self.obstacle_detected:
    #             self.get_logger().warn("Obstacle detected in front! Initiating avoidance maneuver.")
    #             self.avoid_obstacle()

    # def avoid_obstacle(self):
    #     # 장애물 회피를 위한 단순한 회피 동작 예시
    #     # 실제 로봇에서는 로컬 플래너와 통합된 회피 알고리즘 사용
    #     twist = Twist()
    #     twist.linear.x = 0.0
    #     twist.angular.z = -0.5  # 좌회전으로 장애물 회피
    #     self.cmd_vel_publisher.publish(twist)
    #     time.sleep(1)  # 회피 동작 지속 시간
    #     twist.angular.z = 0.0
    #     self.cmd_vel_publisher.publish(twist)
    
    def path_callback(self, msg):
        self.get_logger().info(f"Received path with {len(msg.poses)} points.")

        with self.lock:
            if self.path_following_thread is not None and self.path_following_thread.is_alive():
                self.get_logger().info("Interrupting previous path following.")
                self.nav.cancelTask()
                self.path_following_thread.join()

            self.current_path_poses = msg.poses
            self.last_waypoint_is_home = (msg.poses[-1].pose.position.x == 0.0 and msg.poses[-1].pose.position.y == 0.0)
            
            self.path_following_thread = threading.Thread(target=self.follow_path, args=(msg.poses,))
            self.path_following_thread.start()

    def follow_path(self, poses):
        valid_poses = []

        for i, pose in enumerate(poses):
            if isinstance(pose, PoseStamped):
                valid_poses.append(pose)
                self.get_logger().info(f"Waypoint {i + 1}/{len(poses)}: ({pose.pose.position.x}, {pose.pose.position.y})")
            else:
                self.get_logger().error(f"Invalid pose at index {i}, skipping.")

        if not valid_poses:
            self.get_logger().error("No valid waypoints received, aborting path following.")
            return

        self.set_state(RobotState.MOVING)
        self.nav.followWaypoints(valid_poses)

        while not self.nav.isTaskComplete():
            if self.obstacle_detected:
                self.get_logger().warn("Obstacle in path, waiting for clearance.")
                time.sleep(3)
                continue
            
            if self.current_position is not None:
                target_pose = valid_poses[-1].pose.position
                remaining_distance = math.hypot(
                    target_pose.x - self.current_position.x,
                    target_pose.y - self.current_position.y
                )
                self.get_logger().info(
                    f"Distance remaining to final waypoint: {remaining_distance:.2f} meters"
                )
                with self.lock:
                    if remaining_distance <= 0.05:  
                        self.get_logger().info("Arrived at final waypoint within tolerance")
                        self.arrived = True
                        self.obstacle_detected = False
                        break

            time.sleep(0.05)  

        result = self.nav.getResult()
        if result == TaskResult.SUCCEEDED:
            self.set_state(RobotState.ARRIVED)
            self.stop_robot()
            self.publish_arrival_status()
            # if self.last_waypoint_is_home:
                # self.publish_arrival_at_home()
                
        else:
            self.set_state(RobotState.STOP)
            self.stop_robot()
            self.publish_arrival_status()
    
    def publish_arrival_status(self):
        """Publish a message indicating the robot has arrived at the destination."""
        self.get_logger().info("Robot has arrived at the final destination.")
        msg = Bool()
        msg.data = self.arrived
        self.arrive_publisher.publish(msg)
        time.sleep(0.2)
        self.arrived = False
    
    # def adjustment_complete_callback(self, msg):
    #     if msg.data == 'adjustment_complete':
    #         self.stop_robot()
            # self.set_state(RobotState.STOP)
            # status_msg = TaskProgressUpdate()
    #         status_msg.task_complete = True
    #         self.status_publisher.publish(status_msg)
    #         self.get_logger().info("Requesting next path...")

    def stop_robot(self):
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.linear.y = 0.0
        stop_msg.linear.z = 0.0
        stop_msg.angular.x = 0.0
        stop_msg.angular.y = 0.0
        stop_msg.angular.z = 0.0
        self.cmd_vel_publisher.publish(stop_msg)
        
    # def publish_arrival_at_home(self):
    #     """Publish a message indicating the robot has arrived at home."""
    #     self.set_state(RobotState.AT_HOME)
    #     arrival_msg = String()
    #     arrival_msg.data = "Robot has arrived at home."
    #     self.robot_state_publisher.publish(arrival_msg)
    #     self.get_logger().info("Published arrival at home status.")
        
def main(args=None):
    rclpy.init(args=args)
    node = PathFollower()
    executor = MultiThreadedExecutor()

    try:
        rclpy.spin(node, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

