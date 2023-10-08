# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

class ArrayMerger(Node):

    def __init__(self):
        super().__init__('merge_arrays_node')
        self.subscription = self.create_subscription(
            String,
            '/input/array1',
            self.callback1,
            10)

        self.subscription2 = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.callback2,
            10)
        
        self.publisher = self.create_publisher(
            Int32MultiArray, 
            '/output/array', 
            10)
        self.array1 = []
        self.array2 = []

    def callback1(self, msg):
        self.array1 = msg.data
        self.merge_and_publish()

    def callback2(self, msg):
        self.array2 = msg.data
        self.merge_and_publish()

    def merge_and_publish(self):
        if(len(self.array1) == 0 or len(self.array2) == 0):
            return
        merged_array = sorted(self.array1+self.array2)
        output_array = Int32MultiArray(data = merged_array)
        self.publisher.publish(output_array)

def main(args=None):
    rclpy.init(args=args)
    array_merger_node = ArrayMerger()
    rclpy.spin(array_merger_node)

    array_merger_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
