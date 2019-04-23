import paho.mqtt.client as mqttClient
from sense_hat import SenseHat
import os
import time
import json
 
def convert_c_to_f(c): # Doesn't Work Yet
        return c * 9.0 / 5.0 + 32.0

def measureCPU_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=",""))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")
 
Connected = False
broker_address = "io.adafruit.com"
broker_port = 1883
user = "llindsay971"
password = "893e91577ab34c34b90ab31053642c92"
 
client = mqttClient.Client("Ree2")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.connect(broker_address, port=broker_port)
client.loop_start()
 
while Connected != True:
    time.sleep(1)
 
try:
    while True:
    
        sense = SenseHat()

        p = sense.get_temperature_from_pressure()
        h = sense.get_temperature_from_humidity()

        temperatureA = (p+h) / 2
        
        #print("Average temp test %d",((p+h) / 2))
        
        time.sleep(9)
        strTemp = measureCPU_temp()
        splitTemp = strTemp[0] + strTemp[1] + strTemp[2] + strTemp[3]
        #value = input("Enter the message: ")

        temperatureCPU = float(splitTemp)

        #print(temperatureCPU)

        factor = 5

        temperatureC = round(temperatureA - (temperatureCPU/factor), 1)

        #print("Temperature ",temperatureC)

        Sensor2 = {"id":1, "setTemperature":25, "Temperature":temperatureC}

        print("Test ",json.dumps(Sensor2))
                
        client.publish("llindsay971/feeds/coursework.testingData", json.dumps(Sensor2), qos=0, retain=False)
   
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()

