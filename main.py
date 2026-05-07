import obsws_python as obs
import time
import base64
import io
from PIL import Image, ImageStat

HOST = "localhost"
PORT = 4455
PASSWORD = ""
SLIDES = "Target Element"
VIEWER = "Slides"

client = obs.ReqClient(host=HOST, port=PORT, password=PASSWORD)


def detectBlank() -> bool:
    try:
        image = client.get_source_screenshot(VIEWER, "png", 160, 90, -1)
        image_data = image.image_data
        image_bytes = base64.b64decode(image_data.split(",")[-1])
        img = Image.open(io.BytesIO(image_bytes)).convert('L')

        stat = ImageStat.Stat(img)
        average = stat.mean[0]

        return average < 5.0

    except Exception as e:
        print(f"Error Detecting slide: {e}")


def main() -> None:
    while True:
        current_projection = client.get_current_program_scene()
        current_saved = client.get_current_preview_scene().scene_name
        blank = detectBlank()
        _id = client.get_scene_item_id(current_projection.scene_name, SLIDES).scene_item_id
        change_state = client.get_scene_item_enabled(current_projection.scene_name, _id).scene_item_enabled
        
        
        if change_state == blank:
                
                client.set_current_preview_scene(current_projection.scene_name)

                client.set_scene_item_enabled(current_projection.scene_name, _id, not blank)

                client.set_current_program_scene(current_projection.scene_name)
                client.set_current_preview_scene(current_saved)

      

        time.sleep(0.2)

if __name__ == "__main__":
    main()