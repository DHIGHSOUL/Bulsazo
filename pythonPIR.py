import time
import requests
import RPi.GPIO as GPIO

PIN_PIR = 6
detection = "Not detected!"

def postPIR(detect):
    url = "http://203.253.128.177:7579/Mobius/Bulsazo/Proximity/CMD"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": \"%s\"\n    }\n}" % detect
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'S6uUvi644hj',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def sensePIR(channel):
    postPIR("1")
    detection = "Detected!"
    print(detection)
    stopSensing()
    time.sleep(60)  # Wait for 60 seconds
    startSensing()  # Restart the sensor

def stopSensing():
    GPIO.cleanup()
    GPIO.remove_event_detect(PIN_PIR)

def startSensing():
    postPIR("0")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_PIR, GPIO.IN)
    GPIO.add_event_detect(PIN_PIR, GPIO.RISING, callback=sensePIR)

try:
    startSensing()
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("KeyboardInterrupt")