# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-15 13:49:12

""" Stepper motor driver for Raspberry Pi, Python3 """
import time

import RPi.GPIO as GPIO


class Stepper:
    def __init__(self, A1, A2, B1, B2, steps=200):
        """
        A1, A2: Coil 1 pins
        B1, B2: Coil 2 pins
        steps: Motor steps per revolution
        """
        self.A1 = A1
        self.A2 = A2
        self.B1 = B1
        self.B2 = B2
        self.steps_per_revolution = steps
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.B1, GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)

    def _write_pins(self, a1, a2, b1, b2):
        GPIO.output(self.A1, a1)
        GPIO.output(self.A2, a2)
        GPIO.output(self.B1, b1)
        GPIO.output(self.B2, b2)

    def step(self, n, sps):
        """ Rotate the motor by `n` steps at a rate of `sps` steps per second """
        delay = 1 / (sps * 4)
        for i in range(n):
            self._write_pins(1, 0, 1, 0)
            time.sleep(delay)
            self._write_pins(0, 1, 1, 0)
            time.sleep(delay)
            self._write_pins(0, 1, 0, 1)
            time.sleep(delay)
            self._write_pins(1, 0, 0, 1)
            time.sleep(delay)

    def rotate(rotations, rpm):
        """ Rotate the motor through `rotations` full revolutions at `rpm` revolutions per minute """
        steps = rotations * self.steps_per_revolution
        steps_per_second = rpm / 60 * self.steps_per_revolution
        self.step(steps, steps_per_second)
