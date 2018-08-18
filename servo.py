# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-08-18 10:58:16

import RPI.GPIO as GPIO

class Servo:
    def __init__(self, pin):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.OUTPUT)
        self.pwm = GPIO.PWM(self._pin, 50)  # 50Hz = 20ms period
        self.enabled = False

    def write(self, angle):
        duty_cycle = (angle / 18) + 2.5
        if self.enabled:
            self.pwm.ChangeDutyCycle(duty_cycle)
        else:
            self.enabled = True
            self.pwm.start(duty_cycle)

    def detach(self):
        self.enabled = False
        self.stop()
