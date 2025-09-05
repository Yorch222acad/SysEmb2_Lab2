import RPi.GPIO as GPIO
import time
import random

# Suppress warnings
GPIO.setwarnings(False)

Btn1 = 11
Btn2 = 9
Btn3 = 10 # Reservado para cambio de ejercicio
#-----------------------
Led1 = 0
Led2 = 5
Led3 = 6
Led4 = 13
#-----------------------
PinsBtn = [Btn1, Btn2, Btn3]
PinsLed = [Led1, Led2, Led3, Led4]
#-----------------------
Vent = 27

GPIO.setmode(GPIO.BCM)

for pin in PinsBtn:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in PinsLed:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
GPIO.setup(Vent, GPIO.OUT)

#===================================================================

estado = 1
counter = 0
binAnt = -1
l = [0, 0, 0, 0]
#----------------
estado_led = 1
tiempo = 1

#===================================================================

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

#===================================================================

GPIO.add_event_detect(Btn1, GPIO.FALLING, callback=cambiar_estado, bouncetime=300)
#---------------------
GPIO.add_event_detect(Btn1, GPIO.FALLING, callback=cambiar_led, bouncetime=300)
GPIO.add_event_detect(Btn2, GPIO.FALLING, callback=aumentar_tiempo, bouncetime=300)

#===================================================================

while True:

    if estado == 1:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.HIGH)
        time.sleep(1)

    elif estado == 2:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.LOW)
        time.sleep(2)

    elif estado == 3:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.HIGH)

    elif estado == 4:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.LOW)
    
    time.sleep(0.1)

#//////////////////////////////////////////////////////////////////

    if GPIO.input(Btn1) == GPIO.LOW and counter < 15:
        counter += 1
        time.sleep(0.2)  # debounce

    if GPIO.input(Btn2) == GPIO.LOW and counter > 0:
        counter -= 1
        time.sleep(0.2)  # debounce

    if counter != binAnt:
        l = [0, 0, 0, 0]
        temp = counter
        for j in range(3, -1, -1):  
            l[j] = temp % 2
            temp //= 2
        binAnt = counter

    for idx, pin in enumerate(PinsLed):
        GPIO.output(pin, GPIO.HIGH if l[idx] else GPIO.LOW)

#//////////////////////////////////////////////////////////////////

    temp = random.randint(5, 25)

    if temp < 12:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Vent, GPIO.LOW)
        print(f"La temperatura es {temp}")
    elif temp > 20:
        GPIO.output(Vent, GPIO.HIGH)
        GPIO.output(Led1, GPIO.LOW)
        print(f"La temperatura es {temp}")
    else:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Vent, GPIO.LOW)
        print(f"La temperatura es {temp}")
    
    time.sleep(4)

#//////////////////////////////////////////////////////////////////

    if estado_led == 1:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.LOW)
        GPIO.output(Led3, GPIO.LOW)
        GPIO.output(Led4, GPIO.LOW)
    elif estado_led == 2:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.HIGH)
        GPIO.output(Led3, GPIO.LOW)
        GPIO.output(Led4, GPIO.LOW)
    elif estado_led == 3:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.LOW)
        GPIO.output(Led3, GPIO.HIGH)
        GPIO.output(Led4, GPIO.LOW)
    elif estado_led == 4:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.LOW)
        GPIO.output(Led3, GPIO.LOW)
        GPIO.output(Led4, GPIO.HIGH)
    
    time.sleep(tiempo)
    GPIO.output(Led1, GPIO.LOW)
    GPIO.output(Led2, GPIO.LOW)
    GPIO.output(Led3, GPIO.LOW)
    GPIO.output(Led4, GPIO.LOW)
    time.sleep(1)
