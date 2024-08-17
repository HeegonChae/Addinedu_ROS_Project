#!/usr/bin/env python3

import sys
import os
from ament_index_python.packages import get_package_share_directory

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.executors import MultiThreadedExecutor
from threading import Thread

from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
#from task_msgs.srv import ArucoCommand

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

from tf_transformations import quaternion_from_euler

main_server_gui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main_server_gui'))
# UI 파일 로드
ui_file = os.path.join(main_server_gui_dir, 'share', 'main_server_gui', 'ui', 'qt_controll.ui')
from_class = uic.loadUiType(ui_file)[0]

class RobotGoal(Node):
    def __init__(self, ui):
    
        super().__init__("goal_node")
        # UI 파일 로드
        # uic.loadUi(ui_file, self)

        self.ui = ui
        # self.ui.stepClicked.connect(self.cancel_goal)
        # self.ui.arucoClicked.connect(self.cancel_goal)
        self.ui.goalClicked.connect(self.go_to_goal)

        # 네비게이터 초기화
        self.nav = BasicNavigator()
        self.goal_pose = PoseStamped()

    def go_to_goal(self):
        self.goal_pose.header.frame_id = 'map'
        self.goal_pose.header.stamp = self.nav.get_clock().now().to_msg()
        self.goal_pose.pose.position.x = float(self.ui.goalXEdit.text())
        self.goal_pose.pose.position.y = float(self.ui.goalYEdit.text())
        self.goal_pose.pose.position.z = 0.0
        self.goal_pose.pose.orientation.x = 0.0
        self.goal_pose.pose.orientation.y = 0.0
        self.goal_pose.pose.orientation.z = float(self.ui.orienZEdit.text())
        self.goal_pose.pose.orientation.w = float(self.ui.orienWEdit.text())

        print(self.goal_pose.pose.position.x, self.goal_pose.pose.position.y)
        print()
        print(self.goal_pose.pose.orientation.z, self.goal_pose.pose.orientation.w)
        print("------------------------")
        # # 목표 위치로 이동
        # self.nav.goToPose(self.goal_pose)

        # i = 0
        # while not self.nav.isTaskComplete():
        #     i += 1
        #     feedback = self.nav.getFeedback()
            
        #     if feedback and i % 5 == 0:
        #         print(f'Distance remaining: {feedback.distance_remaining:.2f} meters.')
            
        #     # 네비게이션 타임아웃 설정
        #     if Duration.from_msg(feedback.navigation_time) > Duration(seconds=10.0):
        #         self.nav.cancelTask()
        #         print('Navigation task canceled due to timeout.')
        #         break

        # result = self.nav.getResult()
        # if result == TaskResult.SUCCEEDED:
        #     print('Goal succeeded!')
        # elif result == TaskResult.CANCELED:
        #     print('Goal was canceled!')
        # elif result == TaskResult.FAILED:
        #     print('Goal failed!')

class ControlWidget(QWidget, from_class):
    goalClicked = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("test")
        self.goalXEdit.setText("0.0")
        self.goalYEdit.setText("0.0")
        self.orienXEdit.setText("0.0")
        self.orienYEdit.setText("0.0")
        self.orienZEdit.setText("0.0")
        self.orienWEdit.setText("0.0")

        self.PATH_LIST = {
            'w1' : [0.5, -1.1], 'w2' : [0.5, -0.5], 'w3' : [0.5, 0.3], 'w4' : [0.5, 1.0],
            'w5' : [1.55, -1.1], 'w6' : [1.55, -0.5], 'w7' : [1.55, 0.3], 'w8' : [1.55, 1.0],
        }
        
        self.POSITION_DICT = {
            "I1" : [0.5, -1.425],  "I2" : [0.5, -1.1],  "I3" : [0.5, -0.625],
            "O1" : [1.45, 1.06],   "O2" : [1.45, 0.66],   "O3" : [1.45, 0.46],
            "P3" : [0.3, 1.2],    "P2" : [0.3, 0.7],    "P1" : [0.3, 0.15],
            "R1" : [1.45, -1.4],   "R2" : [1.45, -1.1],
            "A1" : [0.9, 0.3],    "A1_2" : [0.9, 0.3], 
            "A2" : [1.37, 0.3],    "A2_2" : [1.37, 0.3],
            "B1" : [0.9, -0.5],   "B1_2" : [0.9, -0.5], 
            "B2" : [1.37, -0.5],   "B2_2" : [1.37, -0.5],
            "C1" : [0.9, -1.2],   "C1_2" : [0.9, -1.2], 
            "C2" : [1.37, -1.2],   "C2_2" : [1.37, -1.2]
        }

        self.YAW_DICT = {
            "up" : 3.14,    
            "down" : 0.0,    
            "right" : 1.57, 
            "left" : -1.57,
        }

        # set event
        self.btnGo.clicked.connect(self.go_to_goal)
        self.pathCombo.currentIndexChanged.connect(self.path_changed)
        self.pointCombo.currentIndexChanged.connect(self.postion_changed)
        self.orienCombo.currentIndexChanged.connect(self.orien_changed)


    def path_changed(self):
        path = self.pathCombo.currentText()
        coordinates = self.PATH_LIST[path]
        self.goalXEdit.setText(str(coordinates[0]))
        self.goalYEdit.setText(str(coordinates[1]))
        

    def postion_changed(self):
        position = self.pointCombo.currentText()
        coordinates = self.POSITION_DICT[position]
        self.goalXEdit.setText(str(coordinates[0]))
        self.goalYEdit.setText(str(coordinates[1]))

    def orien_changed(self):
        orientation = self.orienCombo.currentText()
        yaw = self.YAW_DICT.get(orientation, 0.0)
        quaternion = quaternion_from_euler(0, 0, yaw)

        self.orienXEdit.setText(str(quaternion[0]))
        self.orienYEdit.setText(str(quaternion[1]))
        self.orienZEdit.setText(str(quaternion[2]))
        self.orienWEdit.setText(str(quaternion[3]))


    def go_to_goal(self):
        self.goalClicked.emit(True)

def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()

    app = QApplication(sys.argv)
    myWindows = ControlWidget()
    myWindows.show()

    goal_node = RobotGoal(myWindows)
    executor.add_node(goal_node)

    thread = Thread(target=executor.spin)
    thread.start()

    try:
        app.exec_()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
