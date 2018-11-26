#!/usr/bin/env python3

import code

from wafflebot import *
from stepper import A4988
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

ps = PowerSupply()
lm = LidMotor()

pump = A4988(step_pin=29, dir_pin=31, steps=200)
pump.set_step_mode(A4988.STEP_SIXTEENTH)

print("WaffleBot Testing")
print("ps: PowerSupply")
print("lm: LidMotor")
print("pump: A4988 Stepper")

try:
    code.interact(local=locals())

finally:
    GPIO.cleanup()
    print("Exiting interactive shell... Cleanup successful")
