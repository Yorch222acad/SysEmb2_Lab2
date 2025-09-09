import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pines
Btn1 = 25  # Cambiar estado
Btn2 = 8   # Cambiar LED
Btn3 = 7   # Aumentar tiempo
Btn4 = 1   # Seleccionar laboratorio
PinsLed = [0, 5, 6, 13]  # LEDs
Vent = 27

# Configuracion pines
PinsBtn = [Btn1, Btn2, Btn3, Btn4]
for pin in PinsBtn:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in PinsLed:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(Vent, GPIO.OUT)

Led1, Led2, Led3, Led4 = PinsLed

# Variables globales
estado = 1
estado_led = 1
tiempo = 1
counter = 0
binAnt = -1
l = [0, 0, 0, 0]
last_states = {Btn1: 1, Btn2: 1, Btn3: 1, Btn4: 1}

# ==================== Funciones botones ====================
def leer_botones():
    global estado, estado_led, tiempo, opcion, counter, binAnt, l, last_states

    # === BOTON 1 ===
    if GPIO.input(Btn1) == GPIO.LOW and last_states[Btn1] == 1:
        estado += 1
        if estado > 4:
            estado = 1
        print(f"Estado actual: {estado}")
    last_states[Btn1] = GPIO.input(Btn1)

    # === BOTON 2 ===
    if GPIO.input(Btn2) == GPIO.LOW and last_states[Btn2] == 1:
        if opcion == 2 and counter > 0:
            counter -= 1
            print(f"Counter = {counter}")
        elif opcion==4:
            estado_led += 1
            if estado_led > 4:
                estado_led = 1
            tiempo = 1
            print(f"Estado de LED: {estado_led}")
    last_states[Btn2] = GPIO.input(Btn2)

    # === BOTON 3 ===
    if GPIO.input(Btn3) == GPIO.LOW and last_states[Btn3] == 1:
        if opcion == 2 and counter < 15:
            counter += 1
            print(f"Counter = {counter}")
        elif opcion ==4:
            tiempo += 1
            print(f"Tiempo aumentado a: {tiempo}")
    last_states[Btn3] = GPIO.input(Btn3)

    # === BOTON 4 ===
    if GPIO.input(Btn4) == GPIO.LOW and last_states[Btn4] == 1:
        opcion = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))
        print(f"Seleccionaste laboratorio {opcion}")
    last_states[Btn4] = GPIO.input(Btn4)
# ==================== Funciones para cada laboratorio ====================
def labo1():
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

def labo2():
    global counter, binAnt, l
    if counter != binAnt:
        l = [0, 0, 0, 0]
        temp = counter
        for j in range(3, -1, -1):
            l[j] = temp % 2
            temp //= 2
        binAnt = counter

    for idx, pin in enumerate(PinsLed):
        GPIO.output(pin, GPIO.HIGH if l[idx] else GPIO.LOW)

def labo3():
    temp = random.randint(5, 25)
    if temp < 12:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Vent, GPIO.LOW)
    elif temp > 20:
        GPIO.output(Vent, GPIO.HIGH)
        GPIO.output(Led1, GPIO.LOW)
    else:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Vent, GPIO.LOW)

    print(f"La temperatura es {temp}")
    time.sleep(1)

def labo4():
    if estado_led == 1:
        GPIO.output(Led1, GPIO.HIGH)

    elif estado_led == 2:
        GPIO.output(Led2, GPIO.HIGH)

    elif estado_led == 3:
        GPIO.output(Led3, GPIO.HIGH)

    elif estado_led == 4:
        GPIO.output(Led4, GPIO.HIGH)

    time.sleep(tiempo)
    GPIO.output(Led1, GPIO.LOW)
    GPIO.output(Led2, GPIO.LOW)
    GPIO.output(Led3, GPIO.LOW)
    GPIO.output(Led4, GPIO.LOW)
    time.sleep(0.5)

# ==================== MAIN ====================
labos = {1: labo1, 2: labo2, 3: labo3, 4: labo4}
opcion = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))

try:
    while True:
        leer_botones()
        labos[opcion]()  # ejecuta el laboratorio seleccionado
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()