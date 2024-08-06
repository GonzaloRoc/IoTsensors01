import random
import time
import json
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message
 

def extract_device_id(input_string):
    # Split the input string by semicolon
    parts = input_string.split(";")
    
    # Iterate through the parts and find the one containing "DeviceId"
    for part in parts:
        if "DeviceId" in part:
            # Extract the value after "DeviceId="
            device_id = part.split("=")[1]
            return device_id.strip()  # Remove any leading/trailing spaces
        

# The device connection string to authenticate the device with your IoT hub.
#CONNECTION_STRING = "HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_Sim_RBpy;SharedAccessKey=xjqnHQnoKEXMSpHOfnivVHboy2K+y6GweAIoTJlb7gs="

CONNECTION_STRING = [
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_1;SharedAccessKey=ccfc78wTNiGeOwhM+CVKyAGZSvCt9aYoOAIoTBJIdwc=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_2;SharedAccessKey=AuBQh4QA6l8avk+2gOG3CKQtdhM/sqWeFAIoTJDaslE=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_3;SharedAccessKey=Xxf9K6d2jvunKTnmHa/E+J5LsYvxDeIQCAIoTFzL1mw=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_4;SharedAccessKey=gJjddfx7fvmqdqvs4OzyJkx+gFkoK30hQAIoTGKOd8c=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_5;SharedAccessKey=97CVrnkLJH3233pNLIM8KAs1iU3QbELUPAIoTJ9mPOY=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_6;SharedAccessKey=pMjySoR76R1cyJavTMxYfbehGv/gE6/gkAIoTBx2t0o=",
"hostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_7;SharedAccessKey=szCvyM4NhUte7+zxc5GXzSRHvEb66BPesAIoTOadZUY=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_8;SharedAccessKey=8co7D2KRP6Jf0xmPzaujda4ommfAJoS27AIoTJBI4IQ=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_9;SharedAccessKey=55EkqSwSfsB3xlFOUBFXf6eHmWXEmcu7wAIoTDJSCNM=",
"HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_sim_10;SharedAccessKey=ZWYeI4WR08gaAFo+uG56f9oYBP4ZcSg17AIoTNbLAxo="]


# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
LOCATION_LIST = ["Nice", "Gordes", "Saint-Tropez", "Saint-Jean-Cap-Ferrat", "Cannes", "Marseille", "Toulouse", "Bordeaux", "Montpellier", "Corsica"]
WINDSPEED = 25
KWH = 0.2
DEVICE_ID = "Device_Sim_RBpy"
TIME_SLEEP = 2
COUNTER = 1

def iothub_client_init():
    # Create an IoT Hub client
    n = 0
    # Create an empty list to store the clients
    clients = []
    for MY_STRING in CONNECTION_STRING:
        clients[n] = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        n += 1
        return clients
    
def iothub_client_telemetry_sample_run():
    try:
        clients = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
 
        while True:
            # Build the message with simulated telemetry values.
            for n, client in enumerate(clients):             
                COUNTER += 1
                telemetry_data_point = {
                     "temperature" : TEMPERATURE + (random.random() * 20),
                     "humidity" : HUMIDITY + (random.random() * 20),
                     "windspeed": WINDSPEED + (random.random() * 10),
                     "location" : LOCATION_LIST[n],
                     "kwh": KWH + (random.random()),
                     "device_id" : DEVICE_ID,
                     "time": datetime.utcnow().isoformat(),
                      "counter_msg" : COUNTER
                }
                message_string = json.dumps(telemetry_data_point)
                message = Message(message_string.encode('ascii'))
 
                # Add a custom application property to the message.
                # An IoT hub can filter on these properties without access to the message body.

                if telemetry_data_point["temperature"] > 35:
                    message.custom_properties["temperatureAlert"] = "1"
                else:
                    message.custom_properties["temperatureAlert"] = "0"

                if telemetry_data_point["windspeed"] > 35:
                    message.custom_properties["windspeedAlert"] = "1"
                else:
                    message.custom_properties["windspeedAlert"] = "0"
    
                #sends the message to the IoT hub
                print(f"Sending message: {message}")
                client[n].send_message(message)
                #print (f "[OK] Message successfully sent to IoT Hub {}".format(message) )
                #print (f "Custom properties: {}".format(message.custom_properties) )
                time.sleep(TIME_SLEEP)
 
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
 
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
