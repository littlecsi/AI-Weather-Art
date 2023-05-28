# main.py -- put your code here!

from machine import Pin
from time import sleep

import network

### MAIN ###
sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
  print('connecting to network...')
  sta_if.active(True)
  sta_if.connect('lianderthalin', 'lianderthalin')
  while not sta_if.isconnected():
    pass

print('network config:', sta_if.ifconfig())

led = Pin(2, Pin.OUT)

while True:
  led.value(not led.value())
  sleep(1)
