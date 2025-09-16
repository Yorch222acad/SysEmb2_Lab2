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
temp = 0 # temperatura
ejr = 0
tIter = 0
h1_1 = True
h1_2 = False
h2_1 = True
h2_2 = False

# ==================== MAIN ====================

def main():
    global ejr
    labos = {1: Ejr1, 2: Ejr2, 3: Ejr3, 4: Ejr4}
    LsBtn1 = LsBtn2 = LsBtn3 = 1
    try:
        for pin in PinsLed:
            GPIO.output(pin, GPIO.LOW)
        ejr = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))
        #-----------------------------------------------------------------------
        while True:
            LsBtn1 = dtcBtn1(LsBtn1)
            LsBtn2 = dtcBtn2(LsBtn2)
            LsBtn3 = dtcBtn3(LsBtn3)
            labos[ejr]()  # ejecuta el laboratorio seleccionado
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# ==================== Funciones botones ====================

def dtcBtn1(LsBtn1):
    global estado, counter, mnl, temp, estado_led, tiempo
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
            mnl=5
            temp=25
        elif ejr==4:
            estado_led += 1
            if estado_led > 4:
                estado_led = 1
            tiempo = 1
            print(f"Estado de LED: {estado_led}")
    LsBtn1 = GPIO.input(Btn1)
    return LsBtn1
#------------------------------------------------------------
def dtcBtn2(LsBtn2):
    global counter, mnl, temp, tiempo
    # === BOTON 2 ===
    if GPIO.input(Btn2) == GPIO.LOW and LsBtn2 == 1:
        if ejr == 2 and counter < 15:
            counter += 1
            print(f"Counter = {counter}")
        elif ejr==3:
            mnl=5
            temp=5
        elif ejr==4:
            tiempo+=1
            print(f"Tiempo aumentado a: {tiempo}")
    LsBtn2 = GPIO.input(Btn2)
    return LsBtn2
#------------------------------------------------------------
def dtcBtn3(LsBtn3):
    global ejr
    # === BOTON 3 ===
    if GPIO.input(Btn3) == GPIO.LOW and LsBtn3 == 1:
        for pin in PinsLed:
            GPIO.output(pin, GPIO.LOW)
        ejr = int(input("Ingrese el laboratorio que quiere ejecutar (1-4): "))
        print(f"Seleccionaste laboratorio {ejr}")
    LsBtn3 = GPIO.input(Btn3)
    return LsBtn3
# ==================== Funciones para cada laboratorio ====================

def Ejr1():
    global estado, h1_1, h1_2, h2_1, h2_2
    if estado == 1 and h1_1==True:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.LOW)
        interactiveDelay(1)
        if tIter==0:
            h1_1=False
            h1_2=True
    elif estado == 1 and h1_2==True:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.HIGH)
        interactiveDelay(1)
        if tIter==0:
            h1_1=True
            h1_2=False

    elif estado == 2 and h2_1==True:
        GPIO.output(Led1, GPIO.HIGH)
        GPIO.output(Led2, GPIO.HIGH)
        interactiveDelay(2)
        if tIter==0:
            h2_1=False
            h2_2=True
    elif estado == 2 and h2_2==True:
        GPIO.output(Led1, GPIO.LOW)
        GPIO.output(Led2, GPIO.LOW)
        interactiveDelay(2)
        if tIter==0:
            h1_1=True
            h1_2=False

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
        tmp = counter
        for j in range(3, -1, -1):
            l[j] = tmp % 2
            tmp //= 2
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
    global estado_led, tiempo
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

# ====================================================

def interactiveDelay(time_sec):
    global tIter
    TotalTimeIter = int(time_sec*10)
    if tIter==0:
        tIter=TotalTimeIter
    time.sleep(0.1)
    tIter-=1

if __name__ == "__main__":
    main()