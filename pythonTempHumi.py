import time
import Adafruit_DHT as DHT
import requests
import json

USING_DHT11 = True
DHT_GPIO = 22

print("Starting temp/humid sensor...")

def getTempHumiCMD():
    while True:
        url = "http://203.253.128.177:7579/Mobius/TempHumi/Temperature/CMD/latest"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'SOrigin'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = json.loads(response.text)

        cmd = json_response['m2m:cin']['con']

        print("TempHumiCMD: ", cmd)

        if cmd == '1':
            getRealTempAndHumi()
        else:
            time.sleep(1)

def postEndSignal():
    url = "http://203.253.128.177:7579/Mobius/TempHumi/Temperature/CMD"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": \"0\"\n    }\n}"
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'S6uUvi644hj',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("PostTempResponse: ", response.text)


def postTemp(temp):
    url = "http://203.253.128.177:7579/Mobius/TempHumi/Temperature/DATA"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": \"%s\"\n    }\n}" % temp
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'S6uUvi644hj',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("PostTempResponse: ", response.text)

def postHumi(humi):
    url = "http://203.253.128.177:7579/Mobius/TempHumi/Humidity/DATA"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": \"%s\"\n    }\n}" % humi
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'S6uUvi644hj',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("PostHumiResponse: ", response.text)

def getRealTempAndHumi():
    while True:
        if USING_DHT11:
            sensor = DHT.DHT11
        else:
            sensor = DHT.DHT22

        humidity, temperature = DHT.read_retry(sensor, DHT_GPIO)
        if humidity is not None and temperature is not None:
            print("Check is good!")
            temp = "{0:.1f}".format(temperature)
            postTemp(temp)
            humi = "{0:.1f}".format(humidity)
            postHumi(humi)
            postEndSignal()
            break
        else:
            print("Checksum error, trying again...")
            time.sleep(2)

getTempHumiCMD()