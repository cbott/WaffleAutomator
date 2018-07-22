# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-15 13:49:12

""" Stepper motor driver for Raspberry Pi, Python3 """
import time

import RPi.GPIO as GPIO


class Stepper:
    """
    Class for controlling a 4-wire bipolar stepper motor through an H-bridge
    """
    STEP_POSITIONS = [[1, 0, 1, 0],
                      [0, 1, 1, 0],
                      [0, 1, 0, 1],
                      [1, 0, 0, 1]]
    NUM_POSITIONS = len(STEP_POSITIONS)

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
        self.current_position = 0
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.B1, GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)

    def _write_pins(self, a1, a2, b1, b2):
        GPIO.output(self.A1, a1)
        GPIO.output(self.A2, a2)
        GPIO.output(self.B1, b1)
        GPIO.output(self.B2, b2)

    def _next_position(self):
        """ Move a single step in the positive direction """
        self.current_position = (self.current_position + 1) % self.NUM_POSITIONS
        _write_pins(*self.STEP_POSITIONS[self.current_position])

    def _prev_position(self):
        """ Move a single step in the negative direction """
        self.current_position = (self.current_position - 1) % self.NUM_POSITIONS
        _write_pins(*self.STEP_POSITIONS[self.current_position])

    def step(self, n, sps):
        """ Rotate the motor by `n` steps at a rate of `sps` steps per second """
        delay = 1 / (sps * 4)
        step_fn = self._next_position if n > 0 else self._prev_position
        for i in range(n):
            step_fn()
            time.sleep(delay)

    def rotate(self, rotations, rpm):
        """ Rotate the motor through `rotations` full revolutions at `rpm` revolutions per minute """
        steps = rotations * self.steps_per_revolution
        steps_per_second = rpm / 60 * self.steps_per_revolution
        self.step(steps, steps_per_second)
