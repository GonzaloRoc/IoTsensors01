import random
import time
import json
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message
 
# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "HostName=iotHubSolarFarm.azure-devices.net;DeviceId=Device_Sim_RBpy;SharedAccessKey=xjqnHQnoKEXMSpHOfnivVHboy2K+y6GweAIoTJlb7gs="



# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
LOCATION = "France"
WINDSPEED = 25
KWH = 0.2
DEVICE_ID = "Device_Sim_RBpy"

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
 
def iothub_client_telemetry_sample_run():
    n = 0
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
 
        while True:
            # Build the message with simulated telemetry values.
            n += 1

            telemetry_data_point = {
                  "temperature" : TEMPERATURE + (random.random() * 20),
                  "humidity" : HUMIDITY + (random.random() * 20),
                  "windspeed": WINDSPEED + (random.random() * 10),
                  "location" : LOCATION,
                  "kwh": KWH + (random.random())
                  "device_id" : DEVICE_ID,
                  "time": datetime.utcnow().isoformat(),
                  "counter_msg" : n
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
            client.send_message(message)
            #print (f "[OK] Message successfully sent to IoT Hub {}".format(message) )
            #print (f "Custom properties: {}".format(message.custom_properties) )

            time.sleep(30)
 
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
 
if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
