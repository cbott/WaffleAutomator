#!/usr/bin/env python3
from dash_button import AmazonDashButton
DASH_BUTTON_CONFIG_FILE = "dash_button_addresses.txt"

def button_press():
    print("Button Pressed YEEEEEEEEEEEPP")

with open(DASH_BUTTON_CONFIG_FILE) as f:
    mac_addresses = f.readlines()

b = AmazonDashButton(mac_addresses, button_press)

print("Doing things!")
