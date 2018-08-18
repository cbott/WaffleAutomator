# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-22
import threading

from stepper import Stepper


class WaffleHarwareManager:
    """ Interact with the real world in such as way as to cook a waffle """
    def __init__(self):
        pass

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
            event_queue.task_done()
        # TODO: Cleanup routine or something. How do threads work even?
