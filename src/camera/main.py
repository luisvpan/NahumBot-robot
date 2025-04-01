import cv2
import base64
from constants import is_simulation_mode, is_cam_simulation_mode, simulated_base64_image

width, height = 640, 500

def obj_data(img):
    image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def get_image(camera):

    ret, frame = camera.read()
    #frame = cv2.resize(frame, (width, height))
    #obj_data(frame)

    #cv2.imshow("FRAME", frame)
    
    frame = cv2.resize(frame, (width, height))
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer)
