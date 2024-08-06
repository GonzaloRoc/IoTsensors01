import Adafruit_DHT
import board
import subprocess
import sys
import time
from azure.iot.device import IoTHubDeviceClient, Message
import json
from datetime import datetime



######################################################################################
# this function checks in first place if the device has access to the public internet.
######################################################################################
def check_ping(host):
    try:
        # Run the ping command with a timeout of 2 seconds
        subprocess.check_output(["ping", "-c", "1", "-W", "2", host])
        return "OK"  # Ping successful
    except subprocess.CalledProcessError:
        return "ERROR"  # Ping failed



######################################################################################
#function connects to an IoThbub in Azure
######################################################################################
def connect_to_iothub(connection_string):
   print(f"- Creating connection to IoT Hub for device")
   device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
   if device_client is  None:
       print(f"- Connection to IoT Hub..................ERROR")
       device_client.disconnect()
   else:
       print(f"- Connection to IoT Hub created..........OK")
       return device_client

       

######################################################################################
# This function  gets the deviceID and the Hostname from the Connection String.
######################################################################################
def extract_info(input_string):
    # Split the string by semicolons
    parts = input_string.split(';')
    # Initialize variables for DeviceId and HostName
    device_id = None
    host_name = None
    # Iterate through the parts
    for part in parts:
        if 'DeviceId=' in part:
            device_id = part.split('=')[1]
        elif 'HostName=' in part:
            host_name = part.split('=')[1]
    return device_id, host_name


######################################################################################
#Function that sends Humidity and Temperature telemetry to Azure IoT hub
#Sensor model: DHT22 AM2302
# ARGUMENTS
#   temperature,humidity = [value from sensor]. 
# 	device_client from the IoT Hub Connection string
# 	n = counter for the message id counter
#	location = location for the JSON message
#	device_id = to name the device
######################################################################################
def send_telemetry_TempHum(temperature, humidity,device_client,n,location,device_id):

    #Build the message with telemetry values.
    telemetry_data_point = {
        "temperature" : temperature,
        "humidity" : humidity,
        "location" : location,
        "device_id" : device_id,
        "time": datetime.utcnow().isoformat(),
        "counter_msg" : n
     }
    message_string = json.dumps(telemetry_data_point)
    message = Message(message_string.encode('ascii'))
    # Add a custom application property to the message.
    # An IoT hub can filter on these properties without access to the message body.
    if telemetry_data_point["temperature"] > 30:
        message.custom_properties["temperatureAlert"] = "true"
    else:
        message.custom_properties["temperatureAlert"] = "false"

    #sends the message to the IoT hub
    client.send_message(message)

    #print("Custom properties...")
    #for prop,value in message.custom_properties.items():
        #print(f"{prop}, {value}")

    device_client.send_message(message)
    print("[OK] Telemetry sent to IoT Hub: {}".format(message) )



######################################################################################
#Function that sends PIR  the telemetry to Azure IoT hub
# Sensor Model: AM312 HC-DR312
# 1 means there is movement, and 0 means that no movement has been detected.  
# ARGUMENTS
#   pir_code = [0,1]. 1 there is movement. 01 there is no light detected
# 	device_client from the IoT Hub Connection string
# 	n = counter for the message id counter
#	location = location for the JSON message
#	device_id = to name the device
######################################################################################
def send_telemetry_PIR(pir_code,device_client,n,location,device_id):
    try:
        # Build the message with telemetry values.
        telemetry_data_point = {
            "pir_code" : pir_code,
            "location" : location,
            "device_id" : device_id,
            "time": datetime.utcnow().isoformat(),
            "counter_msg" : n
        }
        message_string = json.dumps(telemetry_data_point)
        message = Message(message_string.encode('ascii'))


        if telemetry_data_point["pir_code"] == 1:
            message.custom_properties["temperatureAlert"] = "true"
        else:
            message.custom_properties["temperatureAlert"] = "false"

        #        print("Custom properties...")
        #        for prop,value in message.custom_properties.items():
        #            print(f"{prop}, {value}")

        device_client.send_message(message)
        print("[OK] Telemetry sent to IoT Hub: {}".format(message))

    except Exception as error:
        print(f"[ERROR] Error occurred: {error}")
        GPIO.cleanup()  # Move the GPIO cleanup inside the except block

######################################################################################
#Function that sends KY-019 Photo LDR Resistance  telemetry to Azure IoT hub
# 1 means there is light, and 0 means that no light has been detected.  
# ARGUMENTS
#     	photoresistor_code = [0,1]. 0 there is light. 1 there is no light detected
# 	device_client from the IoT Hub Connection string
# 	n = counter for the message id counter
#	location = location for the JSON message
#	device_id = to name the device
######################################################################################
def send_telemetry_PhotoResistor(photoresistor_code,device_client,n,location,device_id):
    try:
        # Build the message with telemetry values.
        telemetry_data_point = {
            "photoresistor_code" : photoresistor_code,
            "location" : location,
            "device_id" : device_id,
            "time": datetime.utcnow().isoformat(),
            "counter_msg" : n
        }
        message_string = json.dumps(telemetry_data_point)
        message = Message(message_string.encode('ascii'))


        if telemetry_data_point["photoresistor_code"] == 0:
            message.custom_properties["photoresistorAlert"] = "true"
        else:
            message.custom_properties["photoresistorAlert"] = "false"

#        print("Custom properties...")
#        for prop,value in message.custom_properties.items():
#            print(f"{prop}, {value}")

        device_client.send_message(message)
        print("[OK] Telemetry sent to IoT Hub: {}".format(message))

    except Exception as error:
        print(f"[ERROR] Error occurred: {error}")
        GPIO.cleanup()  # Move the GPIO cleanup inside the except block
