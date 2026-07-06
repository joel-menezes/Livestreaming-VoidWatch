import obsws_python as obs
from obsws_python.error import OBSSDKError, OBSSDKRequestError
import time
import base64
import io
from PIL import Image, ImageStat
from dotenv import load_dotenv
import os

load_dotenv()

HOST = "localhost"
PORT = 4455
PASSWORD = os.getenv("password")
SLIDES = "Target Element" # Source element that will be hidden/unhidden
VIEWER = "Slides" # Monitoring Source

client = obs.ReqClient(host=HOST, port=PORT, password=PASSWORD)


def detectBlank() -> bool:
    try:
        image = client.get_source_screenshot(VIEWER, "png", 160, 90, -1)
        image_data = image.image_data
        image_bytes = base64.b64decode(image_data.split(",")[-1])
        img = Image.open(io.BytesIO(image_bytes)).convert('L')

        stat = ImageStat.Stat(img)
        average = stat.stddev[0]

        return average < 5.0

    except Exception as e:
        print(f"Error Detecting slide: {e}")
        return False

def main() -> None:
    while True:
        try:
            current_projection = client.get_current_program_scene().scene_name
            current_saved = client.get_current_preview_scene().scene_name
            blank = detectBlank()

            scene_items = client.get_scene_item_list(current_projection).scene_items
            items = [item["sourceName"] for item in scene_items]

            if VIEWER in items:
                _id = client.get_scene_item_id(current_projection, SLIDES).scene_item_id
                change_state = client.get_scene_item_enabled(current_projection, _id).scene_item_enabled
                source_activity = client.get_source_active(SLIDES)
                program_enabled = source_activity.video_active

                if change_state == blank or program_enabled == blank:
                    client.set_current_preview_scene(current_projection)
                    client.set_scene_item_enabled(current_projection, _id, not blank)
                    client.trigger_studio_mode_transition()
                    client.set_current_preview_scene(current_saved)

                
        except KeyboardInterrupt as e:
            break
        except OBSSDKRequestError:
            print("Error: Request Error")
        except OBSSDKError as e:
            print("Error: OBS is not ready")
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

        time.sleep(0.5)

if __name__ == "__main__":
    main()