import Adafruit_DHT
import board
import time
#my own library
from  Custom_IoT_library import check_ping, connect_to_iothub, extract_info, send_telemetry_TempHum
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime


######################################################################################
# Script to capture TEMPERATURE and HUMIDITY values from sensor DHT22              
#
#####################################################################################


######  General Variables   #######################################################

CONNECTION_STRING = "HostName=iotHubSolarFarm.azure-devices.net;DeviceId=dh22_sensor_01;SharedAccessKey=GAKC6ocOCL5GQebotvoatBv1W8cgdT09qAIoTFuL4JM=:"
TIMER_SLEEP  = 5
LOCATION = "France"
TIMER_SLEEP_ERROR = 5
host_to_ping = "google.com"
counter = 1

#####################################################################################



print("")
print("------ Initializing sensor, Press Control-C to quit -----")
device_client = connect_to_iothub(CONNECTION_STRING)
device_id, host_name= extract_info(CONNECTION_STRING)
print(f"- DeviceId= ",device_id)
print(f"- IoT Hub = ",host_name)
print(f"- Location = ",LOCATION)
print(f"- GPIO used = 4")
print(f"- TIME SLEEPER = {TIMER_SLEEP}")
result = check_ping(host_to_ping)
print(f"- Checking internet access.................{result}")

try:
	print(f"- Reading PIN GPIO 4 from  device.........OK")
	dht_device = Adafruit_DHT.DHT22(board.D4)  # D4  pin for data

except RuntimeError as Error:
	print(f"Reading pin Error: (Error)")
	device_client.disconnect()



try:
    print(f"- Starting reading process................OK")
    print(f"------------------------------------------------------------")
    print("")

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            print(f"[{counter}] Reading Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} at ({datetime.now()})")
            counter += 1
            send_telemetry_TempHum(temperature, humidity,device_client, counter,LOCATION,device_id)
            time.sleep(TIMER_SLEEP)  # Wait for 5 seconds before reading again

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
