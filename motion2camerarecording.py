import time
import picamera
from gpiozero import MotionSensor
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime

# Azure Blob Storage configuration
connect_str = 'YOUR_AZURE_STORAGE_CONNECTION_STRING'
container_name = 'YOUR_CONTAINER_NAME'

# Initialize the motion sensor
pir = MotionSensor(4)  # GPIO pin 4

# Initialize the camera
camera = picamera.PiCamera()

def upload_to_azure(file_path, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print("Upload successful!")
    except Exception as ex:
        print(f"An error occurred: {ex}")

def record_video():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f'/home/pi/video_{timestamp}.h264'
    blob_name = f'video_{timestamp}.h264'
    
    camera.start_recording(file_path)
    print("Recording started...")
    time.sleep(10)  # Record for 10 seconds
    camera.stop_recording()
    print("Recording stopped.")
    upload_to_azure(file_path, blob_name)

print("Waiting for motion...")
pir.wait_for_motion()
print("Motion detected!")
record_video()
