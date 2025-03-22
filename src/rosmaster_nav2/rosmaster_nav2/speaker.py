import rclpy
from rclpy.node import Node
from partol_interfaces.srv import SpeechText
import espeakng
import sys

print(sys.path)

class Speaker(Node):
    def __init__(self):
        super().__init__('speaker')
        self.srv = self.create_service(
            SpeechText, 'speech_text', self.speech_text_callback)
        self.speaker = espeakng.Speaker()
        self.speaker.voice = 'en'

    def speech_text_callback(self, request, response):
        self.get_logger().info(f'now reading {request.text}')
        self.speaker.say(request.text)
        self.speaker.wait()
        response.result = True
        return response
    
def main(args=None):
    rclpy.init(args=args)
    speaker = Speaker()
    rclpy.spin(speaker)
    rclpy.shutdown()

