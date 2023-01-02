import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from pytesseract import image_to_string
import cv2

from img2txt.blur_detection import image_blurred

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.subscription = self.create_subscription(Image,
            'cam_data',
            self.listener_callback,
            10)

        self.bridge = CvBridge()
    
    def listener_callback(self, data):
        # Display the message on the console
        image = self.bridge.imgmsg_to_cv2(data)
        image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = image_blurred(image_greyscale)
        # skip blurry images
        if blurred:
            return

        
        cv2.imshow("camera", image)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)

    # destroy
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()