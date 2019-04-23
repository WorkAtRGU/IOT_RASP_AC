import paho.mqtt.client as mqttClient
import time
import json
import RPi.GPIO as GPIO
 
fan_channel_1 = 5
fan_channel_2 = 6
gas_sensor = 13
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_channel_1, GPIO.OUT)
GPIO.setup(fan_channel_2, GPIO.OUT)
GPIO.setup(gas_sensor, GPIO.IN)

GPIO.output(fan_channel_1, GPIO.HIGH)
GPIO.output(fan_channel_2, GPIO.HIGH)


 
def sensor_process(sensorData):
    print("checking data")
    print(GPIO.input(13))
    if(GPIO.input(13) == 1):
        fan_off(1)
        fan_off(2)
    elif (sensorData["Temperature"] > sensorData["setTemperature"]):
        print("turning on fan")
        print(GPIO.input(13))
        fan_on(sensorData["id"])
    else:
        fan_off(sensorData["id"])
        print("Sensor {} has a temp of {} this is within range".format(sensorData["id"], sensorData["Temperature"]))
 
def fan_on(id):
    if (id == 1):
        pin = 5
    elif (id == 2):
        pin = 6
        
    print(pin)
    
    GPIO.output(pin, GPIO.LOW)
    print("fan {} is now active".format(id))
 
def fan_off(id):
    if (id == 1):
        pin = 5
    elif (id == 2):
        pin = 6
        
    print(pin)
    
    GPIO.output(pin, GPIO.HIGH)
    print("fan {} is now off".format(id))

 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
        client.subscribe("llindsay971/feeds/coursework.testingData")
    else:
        print("Connection failed")
 
def on_message(client, userdata, message):
    jsonStr = str(message.payload.decode("UTF-8"))
   
    print("Message received " + jsonStr)
 
    sensorData = json.loads(jsonStr)
    tempData = sensorData["Temperature"]
    sensorID = sensorData["id"]
 
 
    if sensorID == 1:
        print("Hello Sensor 1")
        sensor_process(sensorData)
 
       
       
    elif sensorID == 2:
        print("Hello Sensor 2")
        sensor_process(sensorData)
        #print(tempData)
 
       
    else:
        print("Error")
   
    #test = tempData + 0
 
 
 
    #print("plz work ", tempData
 
 
   
 
   
   
   
Connected = False
broker_address = "io.adafruit.com"
broker_port = 1883
user = "llindsay971"
password = "893e91577ab34c34b90ab31053642c92"
 
client = mqttClient.Client("xxxTentxxxIsDEad")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=broker_port)
client.loop_start()
 
while Connected != True:
    time.sleep(1)
 
 
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()