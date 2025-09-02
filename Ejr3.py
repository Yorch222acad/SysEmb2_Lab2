import RPi.GPIO as GPIO
import time
import random
#Para usar el sensor
# import Adafruit_DHT

led_rojo = 17
vent = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_rojo, GPIO.OUT)
GPIO.setup(vent, GPIO.OUT)

while True:
	temp = random.randint(5, 25)
	
	if temp < 12:
		GPIO.output(led_rojo, GPIO.HIGH)
		GPIO.output(vent, GPIO.LOW)
		print(f"La temperatura es {temp}")
	elif temp > 20:
		GPIO.output(vent, GPIO.HIGH)
		GPIO.output(led_rojo, GPIO.LOW)
		print(f"La temperatura es {temp}")
	else:
		GPIO.output(led_rojo, GPIO.LOW)
		GPIO.output(vent, GPIO.LOW)
		print(f"La temperatura es {temp}")
	
	time.sleep(4)