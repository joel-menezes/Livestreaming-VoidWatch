import obsws_python as obs
import time
import cv2
import numpy as np
import base64

HOST = "localhost"
PORT = 4455
PASSWORD = ""


client = obs.ReqClient(host=HOST, port=PORT, password=PASSWORD)

