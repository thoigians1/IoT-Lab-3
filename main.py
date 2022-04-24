print("ThingsBoard works :3")
import paho.mqtt.client as mqttclient
import time
import json
import serial.tools.list_ports

mess = ""
bbc_port = "" #port iot COM7
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

import random


BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "5FOZ4YtaYnpBB8UY5Bp4"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8")) #receive 
    temp_data = {'value': True}
    cmd = 0
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setLED":
            temp_data['valueLED'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1) #listen here 
            cmd = 1 if jsonobj['params'] == True else 0
        if jsonobj['method'] == "setFan":
            temp_data['valueFAN'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1) #listen here 
            cmd = 3 if jsonobj['params'] == True else 2
        if jsonobj['method'] == "setPump":
            temp_data['valuePUMP'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1) #listen here 

    except:
        pass

#send cmd
    if len(bbc_port) > 0:
        ser.write((str(cmd) + "#").encode())

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    collect_data = {splitData[1]:splitData[2]}
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    print(splitData)


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+") # to get info
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
# hàm gọi hàm connect sau khi kết nối thành công
client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
counter = 0

longitude = 106.6297
latitude = 10.8231

while True:
    collect_data = {'humidity': humi, 'light': light_intesity}

    if len(bbc_port) > 0:
        readSerial()
    
    # temp = random.randint(-60,100)
    # humi = random.randint(0,100)
    # longitude = 106.6297
    # latitude = 10.8231
    # light_intesity += 1
    # client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)

    time.sleep(1)
