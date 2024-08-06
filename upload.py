from picamera2 import Picamera2, Preview
from datetime import datetime
import time
import socket


######### GENERAL VARIABLE  ###############3


if __name__ == "__main__":
    # Create a unique file name based on timestamp and hostname
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
   # Get the hostname of the Raspberry Pi
    hostname = socket.gethostname()
    image_filename = f"{hostname}_image_{timestamp}.jpg"

    print(f"File name = {image_filename}")

    picam2=Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)

    print(f"start preview")
    #picam.start_preview(Preview.QTGL)
    picam2.start_preview(Preview.DRM)

    picam2.start()
    time.sleep(2)
   
    print(f"capturing file {image_filename}")
    picam2.capture_file(image_filename)
