import RPi.GPIO as GPIO
import time
import requests

PIN_TRIG = 23
PIN_ECHO = 24
RANGE_MAX = 400
RANGE_MIN = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_TRIG, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

def postUltrasonic(ultrasonicValue):
    url = "http://203.253.128.177:7579/Mobius/Bulsazo/Ultrasonic/DATA"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": \"%s\"\n    }\n}" % ultrasonicValue
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'S6uUvi644hj',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("PostUltrasonicResponse: ", response.text)

try:
    while True:
        GPIO.output(PIN_TRIG, False)
        time.sleep(1)  # 2 Milliseconds

        GPIO.output(PIN_TRIG, True)
        time.sleep(1) # 20 Microseconds
        GPIO.output(PIN_TRIG, False)

        while GPIO.input(PIN_ECHO) == 0:
            pass
        start_time = time.time()

        while GPIO.input(PIN_ECHO) == 1:
            pass
        T = time.time() - start_time
        L = T / 0.000058  # Convert time to distance
        intL = int(L)

        postUltrasonic(str(intL))

        if RANGE_MAX >= L >= RANGE_MIN:
            print(f"Distance is: {intL} cm")
        else:
            print("-1")

        time.sleep(0.1)  # Delay between measurements

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()