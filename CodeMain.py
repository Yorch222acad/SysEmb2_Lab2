import RPi.GPIO as GPIO
import time
import random

# Suppress warnings
GPIO.setwarnings(False)

BOTON = 5
LED1 = 6
LED2 = 13
#---------------------------
PIN_BTN_UP = 19 
PIN_BTN_DOWN = 26 
PIN_OUTS = [0, 5, 6, 13]
#---------------------------
led_rojo = 17
vent = 27
#---------------------------gi
BOTON_1 = 5
BOTON_2 = 14
LED1 = 19
LED2 = 13
LED3 = 26
LED4 = 6


PIN_Btn = [11, 9, 10]
PIN_Led = [0, 5, 6, 13]

GPIO.setmode(GPIO.BCM)

for pin in PIN_Led:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
for pin in PIN_Btn:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(BOTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BOTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#------------------------------------------
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
#------------------------------------------
GPIO.setup(led_rojo, GPIO.OUT)
GPIO.setup(vent, GPIO.OUT)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)


estado = 1
counter = 0
binAnt = -1
l = [0, 0, 0, 0]
#----------------
estado_led = 1
tiempo = 1

def cambiar_led(channel):
    global estado_led, tiempo
    estado_led += 1
    if estado_led > 4:
        estado_led = 1
    tiempo = 1

def cambiar_estado(channel):
    global estado
    estado += 1
    if estado > 4:
        estado = 1

def aumentar_tiempo(channel):
    global tiempo
    tiempo += 1

GPIO.add_event_detect(BOTON, GPIO.FALLING, callback=cambiar_estado, bouncetime=300)
#---------------------
GPIO.add_event_detect(BOTON_1, GPIO.FALLING, callback=cambiar_led, bouncetime=300)
GPIO.add_event_detect(BOTON_2, GPIO.FALLING, callback=aumentar_tiempo, bouncetime=300)
while True:

    if estado == 1:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.HIGH)
        time.sleep(1)

    elif estado == 2:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        time.sleep(2)

    elif estado == 3:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)

    elif estado == 4:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
    
    time.sleep(0.1)

#==========================================================

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

#==========================================================

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

#==========================================================

    if estado_led == 1:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)
    elif estado_led == 2:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.HIGH)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)
    elif estado_led == 3:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.HIGH)
        GPIO.output(LED4, GPIO.LOW)
    elif estado_led == 4:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.HIGH)
    
    time.sleep(tiempo)
    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)
    time.sleep(1)
