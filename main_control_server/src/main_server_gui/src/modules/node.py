#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

from task_manager.srv import GenerateOrder
from task_manager.msg import DbUpdate, GuiUpdate
# Robot Task Client 로부터 오는 메세지 타입
from robot_state.msg import TaskProgressUpdate                                           # new 0807

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject

from modules.mainwindow import *
from modules.robotstatewindow import *                                                   # new 0807
    
class InboundNode(Node):
    def __init__(self, main_window):
        super().__init__('inbound_node')
        # 'GenerateOrder' 메세지 타입의 서비스 클라이언트
        self.client = self.create_client(GenerateOrder, 'generate_order')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.get_logger().info('Service available, ready to send request.')

        # 'DbUpdate' 메세지 타입의 publisher
        self.publisher = self.create_publisher(DbUpdate, 'db_update_status', 10)

        # 'GuiUpdate' 메세지 타입 subscriber
        self.subscription_update = self.create_subscription(
            GuiUpdate,
            'gui_update',
            self.gui_update_callback,
            10)
        
        # 'TaskProgressUpdate' 메세지 타입 subscriber                               # new 0807
        self.subscription_task_progress_update = self.create_subscription(
            TaskProgressUpdate,
            'send_task_complete_results',
            self.inbound_progress_callback,
            10
        )                                                                         # new 0807

        self.main_window = main_window

        # 8시가 되면은 종이 울린다~
        self.main_window.schedule_signal.connect(self.request_inbound_list)
        # Main_window GUI에 신호 연결
        self.main_window.db_update_signal.connect(self.notify_db_update_complete) 


    def request_inbound_list(self):
        if not self.client:
            self.get_logger().error('Client not initialized')
            return
        request = GenerateOrder.Request()
        try:
            future = self.client.call_async(request)
            future.add_done_callback(self.inbound_list_callback)
            self.get_logger().info('Async request sent')
        except Exception as e:
            self.get_logger().error(f'Failed to send async request: {e}')

    def inbound_list_callback(self, future):
        self.get_logger().info('inbound_list_callback called')
        try:
            response = future.result()
            self.get_logger().info(f'Received response: {response}')
            inbound_list = [{
                "item_id": response.item_ids[i],
                "name": response.names[i],
                "quantity": response.quantities[i],
                "warehouse": response.warehouses[i],
                "rack": response.racks[i],
                "cell": response.cells[i],
                "status": response.statuses[i]
            } for i in range(len(response.item_ids))]
            
            self.get_logger().info(f'Parsed inbound list: {inbound_list}')
            # GUI로 signal 발행
            self.main_window.inbound_list_signal.emit(inbound_list)
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

    def notify_db_update_complete(self, status_message):
        msg = DbUpdate()
        msg.status = status_message
        self.publisher.publish(msg)
        self.get_logger().info('Published DB update status')

    def gui_update_callback(self, msg):
        self.get_logger().info(f'GUI Update signal received for product {msg.product_code} with status {msg.status}')
        self.main_window.inbound_status_db_update_signal.emit()

    ##### 여기서 1개 goal_location 당 입고 완료니 랙 정보 업데이트 하라고 받아야 함 #########
    def inbound_progress_callback(self, msg):                                             # new 0807
        if msg.task_complete:
            self.get_logger().info(f'Task completed at rack: {msg.current_rack}') #  "R_A1"

            self.robot_state_window = RobotStateWindow(self.main_window)                  # new 0807
            # Robot_State_window GUI에 신호 연결
            self.robot_state_window.finish_one_inbound_signal.emit(msg.current_rack)   
