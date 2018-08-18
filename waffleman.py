#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: cbott
# @Date:   2018-07-22
from wafflebot import WaffleHarwareManager
from dash_button import AmazonDashButton

DASH_BUTTON_CONFIG_FILE = "dash_button_addresses.txt"

harware_manager = WaffleHarwareManager()


def main():
    event_queue = queue.Queue()  # TODO: restructure this a lot
    harware_manager.run(event_queue)

    with open(DASH_BUTTON_CONFIG_FILE) as f:
        mac_addresses = f.readlines()
    button = AmazonDashButton(mac_addresses, lambda: event_queue.put("One waffle please"))

    while 1:
        pass


if __name__ == "__main__":
    main()
