#Ejercicio 5
from machine import Pin
import time

led_1 = Pin(2, Pin.OUT)
led_2 = Pin(3, Pin.OUT)
led_3 = Pin(4, Pin.OUT)
led_4 = Pin(5, Pin.OUT)


while True:
    led_1.value(1) 
    time.sleep(1)
    led_2.value(1) 
    time.sleep(1)
    led_3.value(1) 
    time.sleep(1)
    led_4.value(1) 
    time.sleep(1)   
    led_1.value(0)
    led_2.value(0)
    led_3.value(0)
    led_4.value(0)  
    time.sleep(1)  
