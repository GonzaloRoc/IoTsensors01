import RPi.GPIO as GPIO
import board
import sys
import time
from Custom_IoT_library import check_ping, connect_to_iothub, extract_info, send_telemetry_PIR
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

##################################################################################
#script to capture the PIR  values from sensor AM312 Mini decteor odule HC-SR312.# 
#
##################################################################################


#####   General variables & initialization #######################################
GPIO_PIN = 15
CONNECTION_STRING = "HostName=iotHubSolarFarm.azure-devices.net;DeviceId=PIRsensor;SharedAccessKey=2gV0gwHeIFgI69HlEGh8Xg+A+3qahJ15KAIoTFDSHVk="
LOCATION = "France"
TIMER_SLEEP = 5
TIMER_SLEEP_ERROR = 5
counter = 1
pir_code = 0
host_to_ping = "google.com"

##################################################################################



#define output file - stored locally
#user_input = input("Enter the name of the file: ")
#sys.stdout = open(user_input, 'w')


# Initialize PIR sensor
print("")
print("------ Initialize PIR sensor, Press Control-C to quit -----")
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

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


try:
    print(f"- Starting reading process...............OK")
    print(f"-----------------------------------------------------------")
    print("")
    while True:
        try:
          
            if GPIO.input(GPIO_PIN):
                print(f"[{counter}], Motion detected! at ({datetime.now()})")
                code = 1
                send_telemetry_PIR(code,device_client,counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)
            else:
                print(f"[{counter}], No motion at ({datetime.now()})")
             
                code = 0
                send_telemetry_PIR(code,device_client,counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)
            counter += 1

        except RuntimeError as error:
            print(f"[ERROR]error ocurred: {error}")
            time.sleep(TIMER_SLEEP_ERROR)  # Retry after 5 seconds

        except Exception as error:
            print(f"Exception occurred: {error}")
            time.sleep(TIMER_SLEEP_ERROR)

except KeyboardInterrupt:
    print("Control-C has been pressed: Exiting due to keyboard interrupt")
finally:
    device_client.disconnect()
    GPIO.cleanup()
