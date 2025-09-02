import RPi.GPIO as GPIO
import time

# Suppress warnings
GPIO.setwarnings(False)

# Configuración de pines (ajusta según tu wiring)
PIN_BTN_UP = 19      # equivalente a PJ0
PIN_BTN_DOWN = 26    # equivalente a PJ1
PIN_OUTS = [0, 5, 6, 13]  # 4 LEDs: PN1, PN0, PF4, PF0 (ejemplo)

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
    # Botón UP → incrementa contador (máximo 15)
    if GPIO.input(PIN_BTN_UP) == GPIO.LOW and counter < 15:
        counter += 1
        time.sleep(0.2)  # debounce

    # Botón DOWN → decrementa contador (mínimo 0)
    if GPIO.input(PIN_BTN_DOWN) == GPIO.LOW and counter > 0:
        counter -= 1
        time.sleep(0.2)  # debounce

    # Si cambió el valor, recalculamos binario
    if counter != binAnt:
        l = [0, 0, 0, 0]
        temp = counter
        for j in range(3, -1, -1):  # de 3 a 0
            l[j] = temp % 2
            temp //= 2
        binAnt = counter

    # Escribir en pines
    for idx, pin in enumerate(PIN_OUTS):
        GPIO.output(pin, GPIO.HIGH if l[idx] else GPIO.LOW)