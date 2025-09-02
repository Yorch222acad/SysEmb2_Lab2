import RPi.GPIO as GPIO
import time

# Suppress warnings
GPIO.setwarnings(False)

# Configuración de pines 
PIN_BTN_UP = 19 
PIN_BTN_DOWN = 26
PIN_OUTS = [0, 5, 6, 13] 

# Inicialización
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in PIN_OUTS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

counter = 0
binAnt = -1
l = [0, 0, 0, 0]


while True:
    if GPIO.input(PIN_BTN_UP) == GPIO.LOW and counter < 15:
        counter += 1
        time.sleep(0.2)  # debounce

    if GPIO.input(PIN_BTN_DOWN) == GPIO.LOW and counter > 0:
        counter -= 1
        time.sleep(0.2)  # debounce

    if counter != binAnt:
        l = [0, 0, 0, 0]
        temp = counter
        for j in range(3, -1, -1):  
            l[j] = temp % 2
            temp //= 2
        binAnt = counter

    for idx, pin in enumerate(PIN_OUTS):
        GPIO.output(pin, GPIO.HIGH if l[idx] else GPIO.LOW)