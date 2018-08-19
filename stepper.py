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


class A4988:
    """ Controller for the A4988 stepper motor driver """
    STEP_FULL = 1
    STEP_HALF = 2
    STEP_QUARTER = 4
    STEP_EIGHTH = 8
    STEP_SIXTEENTH = 16

    def __init__(self, step_pin: int, dir_pin: int, steps: int, ms1=None, ms2=None, ms3=None):
        """
        Initialize the A4988 driver
        ms[1-3]: Microstep mode selection pins
        """
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.steps = steps
        self.ms1 = ms1
        self.ms2 = ms2
        self.ms3 = ms3
        self._mode = self.STEP_FULL  # defalt to full-stepping

        self._mode_controllable = False
        ms_pins = (self.ms1, self.ms2, self.ms3)
        if any(pin is not None for pin in ms_pins):
            if not all(pin is not None for pin in ms_pins):
                raise ValueError("Must provide either all or none of arguments ms1, ms2, ms3")
            self._mode_controllable = True
            for pin in ms_pins:
                GPIO.setup(pin, OUTPUT)

        GPIO.setup(self.step_pin, OUTPUT)
        GPIO.setup(self.dir_pin, OUTPUT)

    def _set_mode_pins(self, a, b, c):
        if not self._mode_controllable:
            # If harware is not configured for setting mode, skip writing to the pins
            return
        GPIO.output(self.ms1, a)
        GPIO.output(self.ms2, b)
        GPIO.output(self.ms3, c)

    def set_step_mode(self, mode):
        """
        Set the step mode
        mode should be one of A4988.[STEP_FULL, STEP_HALF, STEP_QUARTER, STEP_EIGHTH, STEP_SIXTEENTH]

        If mode select pins were not configured, mode will be used for internal
        calculation only with no hardware effecs
        """
        if mode == self.STEP_FULL:
            self._set_mode_pins(GPIO.LOW, GPIO.LOW, GPIO.LOW)
        elif mode == self.STEP_HALF:
            self._set_mode_pins(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
        elif mode == self.STEP_QUARTER:
            self._set_mode_pins(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
        elif mode == self.STEP_EIGHTH:
            self._set_mode_pins(GPIO.HIGH, GPIO.HIGH, GPIO.LOW)
        elif mode == self.STEP_SIXTEENTH:
            self._set_mode_pins(GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
        else:
            raise ValueError("Invalid mode: {}".format(mode))
        self._mode = mode

    def step(self, n: int, sps: float):
        """ Rotate the motor by `n` steps at a rate of `sps` steps per second """
        if sps <= 0:
            raise ValueError("Invalid parameter sps={}. Cannot have zero or negative steps per second".format(sps))
        delay = 1 / (sps * 2)

        if n < 0:
            GPIO.output(self.dir_pin, GPIO.LOW)
        else:
            GPIO.output(self.dir_pin, GPIO.HIGH)

        for i in range(n):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)

    def rotate(self, rotations, rpm):
        """ Rotate the motor through `rotations` full revolutions at `rpm` revolutions per minute """
        microsteps_per_revolution = self.steps * self._mode
        target_steps = rotations * microsteps_per_revolution
        steps_per_second = rpm / 60 * microsteps_per_revolution
        self.step(target_steps, steps_per_second)
