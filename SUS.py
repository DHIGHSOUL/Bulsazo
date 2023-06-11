import threading
import pythonUltrasonic
import getWeather
import requests
import json
import time

sendCMDURLs = [
    'http://203.253.128.177:7579/Mobius/Bulsazo/Ultrasonic/CMD'
    'http://203.253.128.177:7579/Mobius/Bulsazo/LED/CMD'
    'http://203.253.128.177:7579/Mobius/TempHumi/Temperature/CMD'
]

def runPythonUltrasonic():
    pythonUltrasonic.run()

def runGetWeather():
    getWeather.run()

def startThread():
    if __name__ == '__main__':
        thread1 = threading.Thread(target=runPythonUltrasonic)
        thread2 = threading.Thread(target=runGetWeather)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

def sendCMD():
    for cnt in sendCMDURLs:
        url = cnt

        payload = "{\n    \"m2m:cin\": {\n        \"con\": \"1\"\n    }\n}"
        headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'S6uUvi644hj',
        'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("sendCMDResponse: ", response.text)
        time.sleep(1)
    startThread()

def getPIRCMD():
    while True:
        url = "http://203.253.128.177:7579/Mobius/Bulsazo/Proximity/CMD/latest"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SOrigin'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        CMD = response['m2m:cin']['con']

        if CMD == '1':
            sendCMD()
            time.sleep(3)
        else:
            time.sleep(1)

# GET command from Mobius per 1 second

getPIRCMD()