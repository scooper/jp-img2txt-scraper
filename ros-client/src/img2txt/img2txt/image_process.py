import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from custom_msg.msg import ImageMetadata
from cv_bridge import CvBridge
from pytesseract import image_to_string
import cv2

from img2txt.blur_detection import is_image_blurred

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.subscription = self.create_subscription(Image,
            'cam_data',
            self.listener_callback,
            1)
        self.publisher_ = self.create_publisher(ImageMetadata, 'image_metadata', 10)

        self.bridge = CvBridge()
    
    def listener_callback(self, data):
        # Display the message on the console
        image = self.bridge.imgmsg_to_cv2(data)
        image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = is_image_blurred(image_greyscale)
        # skip blurry images
        if blurred:
            return

        gaussian_blur = cv2.GaussianBlur(image_greyscale,(5,5),0)
        adaptive_thresh = cv2.adaptiveThreshold(gaussian_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

        # perform OCR
        result = image_to_string(adaptive_thresh, 'jpn')
        # remove whitespace and filter for kanji
        result = ''.join(result.split())

        if result == '':
            return

        # publish message
        message = ImageMetadata()
        message.ocr_txt = result
        message.image = data
        self.publisher_.publish(message)

        self.get_logger().info(result)
        cv2.imshow("camera", adaptive_thresh)
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