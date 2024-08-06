import RPi.GPIO as GPIO
import board
import sys
import time
from Custom_IoT_library import check_ping, connect_to_iothub, extract_info, send_telemetry_PhotoResistor
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

##################################################################################
#script to capture the Photo sensor  values from sensor AM312 Mini decteor 
#module HC-SR312
#
##################################################################################


#####   General variables & initialization #######################################
GPIO_PIN = 16
CONNECTION_STRING="HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Photoresistor_1;SharedAccessKey=tAQ4oz5jDf+EGYlQxQ7PE6GZw92sEamzhAIoTNprhsE="
LOCATION = "France"
TIMER_SLEEP = 5
TIMER_SLEEP_ERROR = 5
counter = 1
code = 0
host_to_ping = "google.com"

##################################################################################



#define output file - stored locally
#user_input = input("Enter the name of the file: ")
#sys.stdout = open(user_input, 'w')


# Initialize  sensor
print("")
print("------ Initialize Photoresistor sensor, Press Control-C to quit -----")
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

print(f"- Creating connection to IoT Hub for device")
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

print(f"- Connection to IoT Hub created...............OK")
device_id, host_name= extract_info(CONNECTION_STRING)

print(f"- DeviceId= ",device_id)
print(f"- IoT Hub = ",host_name)
print(f"- Location= ",LOCATION)
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
            if GPIO.input(GPIO_PIN)== 0:
                #print(f"value is=",GPIO.input(GPIO_PIN))
                print(f"[{counter}], Light detected! at ({datetime.now()})")
                code = 1
                counter += 1
                send_telemetry_PhotoResistor(code, device_client, counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)
            else:
                print(f"[{counter}], No Light detected at ({datetime.now()})")
                counter += 1
                code = 0
                send_telemetry_PhotoResistor(code, device_client, counter,LOCATION,device_id)
                time.sleep(TIMER_SLEEP)

        except RuntimeError as error:
            print(f"[ERROR]error ocurred: {error}")
            time.sleep(TIMER_SLEEP_ERROR)  

        except Exception as error:
            print(f"Exception occurred: {error}")
            time.sleep(TIMER_SLEEP_ERROR)

except KeyboardInterrupt:
    print("Control-C has been pressed: Exiting due to keyboard interrupt")
finally:
    device_client.disconnect()
    GPIO.cleanup()
