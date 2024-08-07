import time
import picamera
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from datetime import datetime

######################   General variables & initialization #######################################
GPIO_PIN = 15
CONNECTION_STRING = "HostName=iotHubSolarFarm.azure-devices.net;DeviceId=PIRsensor;SharedAccessKey=2gV0gwHeIFgI69HlEGh8Xg+A+3qahJ15KAIoTFDSHVk="
LOCATION = "France"
TIMER_SLEEP = 3
TIMER_SLEEP_ERROR = 5
TIMER_RECORDING = 10
counter = 1
pir_code = 0
host_to_ping = "google.com"

# Azure Blob Storage configuration
connect_str = 'DefaultEndpointsProtocol=https;AccountName=streamingstorage01;AccountKey=xCzH8BpdUgYCw1TZRlTIt3lWEG+S2bkn9tEOuLE8SgQwJc+PulEgf7unavgEXNiTV6VIrm5+WS9X+AStQMTREQ==;EndpointSuffix=core.windows.net'
container_name = 'recordings'


###################################################################################################


# Initialize PIR sensor
print("")
print("------ Initialize PIR sensor, Press Control-C to quit -----")
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)
pir = MotionSensor(GPIO_PIN)  # GPIO pin 

print(f"- Creating connection to IoT Hub for device")
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
print(f"- Connection to IoT Hub created...............OK")
device_id, host_name= extract_info(CONNECTION_STRING)
print(f"- DeviceId= ",device_id)
print(f"- IoT Hub = ",host_name)
print(f"- Location = ",LOCATION)
print(f"- GPIO used = {GPIO_PIN}")
print(f"- TIME SLEEPER = {TIMER_SLEEP}")
result = check_ping(host_to_ping)
print(f"- Checking internet access...............{result}")



# Initialize the camera
camera = picamera.PiCamera()

###################################################################################################
# This function uploads the video to the specified storage account
###################################################################################################
def upload_to_azure(file_path, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print("Upload successful!")
    except Exception as ex:
        print(f"[ERROR] An error occurred: {ex}")

###################################################################################################
# This function records a video and uploads the recording to the Azure storage account
# it records for TIME_RECORDING parameters
# the name of the recording is based on the timestamp creation of the recording
###################################################################################################
def record_video():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f'/home/pi/video_{timestamp}.h264'
        blob_name = f'video_{timestamp}.h264'
        
        camera.start_recording(file_path)
        print("Recording started...")
        time.sleep(TIMER_RECORDING)
        camera.stop_recording()
        print("Recording stopped.")
        upload_to_azure(file_path, blob_name)

###################################################################################################
# runs the script in a loop until Control-C is pressed. 
###################################################################################################
try:
    while True:
        try:      
            #if motion detected by the sensor
            if GPIO.input(GPIO_PIN):
                print(f"[{counter}], Motion detected! at ({datetime.now()})")
                code = 1
                #record the video and upload the video to the azure storage account
                record_video() 
                #send_telemetry_PIR(code,device_client,counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)  # Sleep for a while before checking for motion again
            
            #otherwise let it go till the next round
            else:
                print(f"[{counter}], No motion at ({datetime.now()})")
                code = 0
                #send_telemetry_PIR(code,device_client,counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)
            counter += 1
             
            except RuntimeError as error:
                print(f"[ERROR]error ocurred: {error}")
                time.sleep(TIMER_SLEEP_ERROR)  # Retry after seconds
        
            except Exception as error:
                print(f"[ERROR] Exception occurred: {error}")
                time.sleep(TIMER_SLEEP_ERROR)  # Retry after seconds

except KeyboardInterrupt:
        print("Control-C has been pressed: Exiting due to keyboard interrupt")

finally:
    device_client.disconnect()
    GPIO.cleanup()
