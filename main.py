import obsws_python as obs
import time
import cv2
import numpy as np
import base64
import io
from PIL import Image, ImageStat

HOST = "localhost"
PORT = 4455
PASSWORD = ""
SLIDES = "Target Element"

client = obs.ReqClient(host=HOST, port=PORT, password=PASSWORD)

print(client.get_current_program_scene().current_program_scene_name)

def detectBlank() -> bool:
    try:
        image = client.get_source_screenshot("Slides", "png", 160, 90, -1)
        image_data = image.image_data
        image_bytes = base64.b64decode(image_data.split(",")[-1])
        img = Image.open(io.BytesIO(image_bytes)).convert('L')

        stat = ImageStat.Stat(img)
        average = stat.mean[0]

        return average < 5.0

    except Exception as e:
        print(f"Error Detecting slide: {e}")


def main() -> None:
    pass

if __name__ == "__main__":
    main()