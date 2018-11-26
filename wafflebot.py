# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-22
import threading
import time

import RPi.GPIO as GPIO

from stepper import A4988

PS_EN_PIN = 33
LID_UP_PIN = 35
LID_DOWN_PIN = 37
PUMP_STEP_PIN = 29
PUMP_DIR_PIN = 31
PUMP_NUM_STEPS = 200

HEATUP_TIME = 10  #seconds for iron to get up to temperature from cold
COOK_TIME = 10
LID_RAISE_TIME = 10
LID_LOWER_TIME = 9

class WaffleHarwareManager:
    """ Interact with the real world in such as way as to cook a waffle """
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.lm = LidMotor()
        self.ps = PowerSupply()
        self.pump = A4988(step_pin=PUMP_STEP_PIN, dir_pin=PUMP_DIR_PIN, steps=PUMP_NUM_STEPS)
        self.pump.set_step_mode(A4988.STEP_SIXTEENTH)

    def run(self, event_queue):
        """ Spawn a new process to handle harware tasks in a non-blocking fashion """
        self.event_queue = event_queue
        self.process = threading.Thread(target=self._run)
        self.process.start()
        # TODO: Should this just be done in __init__?

    def _run(self):
        """ Actually do the stuff. TODO: Probably rename """
        while 1:
            task = self.event_queue.get()  # Wait for WaffleMan to tell us what to do
            # Make the waffle!
            self.ps.enable()
            print("Heating...")
            time.sleep(HEATUP_TIME)  #TODO: feedback loop here
            self.lm.up(LID_RAISE_TIME)
            self.pump.rotate(5, 80)  # Pump batter into waffle iron
            self.pump.rotate(-0.5, 200)  # Backrdive a bit to prevent spilling
            self.lm.down(LID_LOWER_TIME)
            print("Cooking...")
            time.sleep(COOK_TIME)
            self.lm.up(LID_RAISE_TIME)
            self.ps.disable()
            self.event_queue.task_done()
        # TODO: Cleanup routine or something. How do threads work even?

    def __del__(self):
        GPIO.cleanup()
        print("Wafflebot destroyed... cleanup successful")


class PowerSupply:
    def __init__(self):
        GPIO.setup(PS_EN_PIN, GPIO.OUT)

    def enable(self):
        GPIO.output(PS_EN_PIN, GPIO.HIGH)

    def disable(self):
        GPIO.output(PS_EN_PIN, GPIO.LOW)

class LidMotor:
    def __init__(self):
        GPIO.setup(LID_UP_PIN, GPIO.OUT)
        GPIO.setup(LID_DOWN_PIN, GPIO.OUT)

    def up(self, t=1):
        start_t = time.time()
        GPIO.output(LID_UP_PIN, GPIO.HIGH)
        try:
            while time.time() - start_t < t:
                time.sleep(0.001)
        finally:
            GPIO.output(LID_UP_PIN, GPIO.LOW)

    def down(self, t=1):
        start_t = time.time()
        GPIO.output(LID_DOWN_PIN, GPIO.HIGH)
        try:
            while time.time() - start_t < t:
                time.sleep(0.001)
        finally:
            GPIO.output(LID_DOWN_PIN, GPIO.LOW)




