import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraData(Node):
    def __init__(self):
        super().__init__('cam_data')
        self.publisher_ = self.create_publisher(Image, 'cam_data', 1)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
    
    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(frame))
        self.get_logger().info("Published Video Frame")


def main(args=None):
    rclpy.init(args=args)
    cam_data = CameraData()
    rclpy.spin(cam_data)

    # destroy
    cam_data.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()