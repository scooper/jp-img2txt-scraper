import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from custom_msg.msg import ImageMetadata
import requests
import uuid
from cv_bridge import CvBridge
import cv2
import re

# localhost for now
URI = "http://127.0.0.1:8000/"

# regular expressions ranges
kanji = r'[㐀-䶵一-鿋豈-頻]'
radicals = r'[⺀-⿕]'

class ImageSender(Node):
    def __init__(self):
        super().__init__('image_sender')
        self.subscription = self.create_subscription(ImageMetadata,
            'image_metadata',
            self.listener_callback,
            50)
        self.bridge = CvBridge()
        self._loop_rate = self.create_rate(2, self.get_clock())
    
    def listener_callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data.image)
        image_file = cv2.imencode('.jpg', cv_image)[1]
        
        image_id = str(uuid.uuid4())

        ocr_txt = data.ocr_txt
        characters = re.findall('(' + kanji + '|' + radicals + ')', data.ocr_txt)


        if characters != '':
            file_to_send = {"file":(image_id + '.jpg', image_file)}

            img_response = requests.post(URI + "upload-image", files=file_to_send)
            self.get_logger().info("Sending Image: " + str(img_response.status_code))
            img_db_response = requests.put(URI + 'api/image', json={"image_id": image_id, "ocr_txt": ocr_txt})
            self.get_logger().info("Adding image to DB: " + str(img_db_response.status_code))

            self._loop_rate.sleep()

            for c in characters:
                c_payload = {"image_id": image_id, "character": c}
                char_response = requests.put(URI + 'api/character', json=c_payload)
                self.get_logger().info("Adding character to DB: " + str(char_response.status_code))

def main(args=None):
    rclpy.init(args=args)
    image_sender = ImageSender()
    rclpy.spin(image_sender)

    # destroy
    image_sender.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()