import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from custom_msg.msg import ImageMetadata
import requests
import uuid
from cv_bridge import CvBridge
import cv2

# localhost for now
URI = "http://127.0.0.1:8000/"

class ImageSender(Node):
    def __init__(self):
        super().__init__('image_sender')
        self.subscription = self.create_subscription(ImageMetadata,
            'image_metadata',
            self.listener_callback,
            50)
        self.bridge = CvBridge()
    
    def listener_callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data.image)
        image_file = cv2.imencode('.jpg', cv_image)[1]
        
        ocr_txt = data.ocr_txt
        file_to_send = {"file":(str(uuid.uuid4()) + '.jpg', image_file)}
        response = requests.post(URI + "upload-image", files=file_to_send)


def main(args=None):
    rclpy.init(args=args)
    image_sender = ImageSender()
    rclpy.spin(image_sender)

    # destroy
    image_sender.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()