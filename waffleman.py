#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-22
import queue
import time

from wafflebot import WaffleHarwareManager
from dash_button import AmazonDashButton

DASH_BUTTON_CONFIG_FILE = "dash_button_addresses.txt"

harware_manager = WaffleHarwareManager()
event_queue = queue.Queue()  # TODO: restructure this a lot


def command_waffle():
    print("Requesting Waffle from wafflebot")
    event_queue.put("One waffle please")


def main():
    harware_manager.run(event_queue)

    #mac_addresses = []
    #try:
    #    with open(DASH_BUTTON_CONFIG_FILE) as f:
    #        mac_addresses = f.readlines()
    #except FileNotFoundError:
    #    pass
    #button = AmazonDashButton(mac_addresses, command_waffle)

    while 1:
        print("Waffleman mainloop... Waiting for user event")
        req = input("Waffle [Y/n]?")
        if req != "Y":
            break
        command_waffle()


if __name__ == "__main__":
    main()
