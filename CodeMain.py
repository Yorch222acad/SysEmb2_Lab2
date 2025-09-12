import RPi.GPIO as GPIO
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pines
Btn1 = 8
Btn2 = 7
Btn3 = 1   # Seleccionar laboratorio
#-----------------------------------
Led1 = 0
Led2 = 5
Led3 = 6
Led4 = 13
#-----------------------------------
PinsLed = [Led1, Led2, Led3, Led4]
PinsBtn = [Btn1, Btn2, Btn3]
Vent = 25

# Configuracion pines
for pin in PinsBtn:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in PinsLed:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(Vent, GPIO.OUT)

# Variables globales
estado = 1
estado_led = 1
tiempo = 1
counter = 0
binAnt = -1
l = [0, 0, 0, 0]
mnl = 0
temp = 0

# ==================== Funciones botones ====================
# global estado, estado_led, tiempo, opcion, counter, binAnt, l, mnl, temp

def dtcBtn1(ejr):
    LsBtn1 = 1
    if GPIO.input(Btn1) == GPIO.LOW and LsBtn1 == 1:
        if ejr==1:
            estado += 1
            if estado > 4:
                estado = 1
            print(f"Estado actual: {estado}")
        elif ejr==2 and counter>0:
            counter -= 1
            print(f"Counter = {counter}")
        elif ejr==3:
            mnl=3
            temp=25
        elif ejr==4:
            estado_led += 1
            if estado_led > 4:
                estado_led = 1
            tiempo = 1
            print(f"Estado de LED: {estado_led}")
    LsBtn1 = GPIO.input(Btn1)
#------------------------------------------------------------
def dtcBtn2():
    LsBtn2 = 1
    # === BOTON 2 ===
    if GPIO.input(Btn2) == GPIO.LOW and LsBtn2 == 1:
        if opcion == 2 and counter < 15:
            counter += 1
            print(f"Counter = {counter}")
        elif opcion==3:
            mnl=3
            temp=5
        elif opcion==4:
            tiempo+=1
            print(f"Tiempo aumentado a: {tiempo}")
    LsBtn2 = GPIO.input(Btn2)
#------------------------------------------------------------
def dtcBtn3():
    LsBtn3 = 1
    # === BOTON 3 ===
    if GPIO.input(Btn3) == GPIO.LOW and LsBtn3 == 1:
        opcion = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))
        print(f"Seleccionaste laboratorio {opcion}")
    LsBtn3 = GPIO.input(Btn3)

# ==================== Funciones para cada laboratorio ====================

def Ejr1():
    LsBtn3 = 1
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

def Ejr2():
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

def Ejr3():
    global mnl, temp
    if mnl==0:
        temp = random.randint(5, 25)
    else:
        mnl-=1
    #---------------------------------
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

def Ejr4():
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

labos = {1: Ejr1, 2: Ejr2, 3: Ejr3, 4: Ejr4}
ejr = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))

try:
    while True:
        dtcBtn1(ejr)
        dtcBtn2(ejr)
        dtcBtn3(ejr)
        labos[ejr]()  # ejecuta el laboratorio seleccionado
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()