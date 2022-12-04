import faulthandler
from gpiozero import Button
import time

t = 1

# This is a mapping based on the jukebox keypad circuitry
# Seeburg Tabletop Jukebox keypad
"""Pins triggered in pairs based on circuitry
ZERO = [5, 3], [7, 2]
ONE = [17.3], [14, 8]
TWO = [15, 9], [3, 12]
THREE = [16, 10], [3, 13]
FOUR = [11, 7], [11, 10]
FIVE = [11, 9], [11, 10]
SIX = [11, 10], [11, 8]
SEVEN = [11, 7], [11, 8]
EIGHT = [9, 6], [8, 6]
NINE = [9, 6], [7, 6]
RESET = [4, 1], [4, 1]
"""

# Summarize the list of different pins triggered for each key pressed.
# Buttons pushed will complete a circuit on each pair of pins.
# Assumes voltage applied to following pins on the keypad : 1,2,3,6,11,14,15,16

keyPins = {
    # keyboard pin : gpio pin
    4: 21,
    5: 20,
    7: 16,
    8: 12,
    9: 26,
    10: 19,
    12: 13,
    13: 6,  # test
    17: 5,
}


def setPins():
    print("Setting Pin defaults")
    for x in keyPins.keys():
        gpio = keyPins[x]
        Button(gpio, pull_up=False)


def check_all():
    for x in keyPins.keys():  # itterates through the keys (keyboard pins)
        gpio = keyPins[x]
        button = Button(gpio, pull_up=False)
        # print(f"{x},", end="")
        # print(f"Checking key:{x} gpio:{gpio}", end="")  # debug
        # print(button.is_pressed)
        if button.value:
            print(f"Activated: keyPadPinout:{x} - gpio:{gpio}")

    print("_______________________")
    # print("Repeat")


setPins()
print("### Press buttons slowly. Wait for Attempt to itterate ")
while True:

    try:
        # print(f"#### Attempts: {t}") #debug
        faulthandler.enable()
        triggerPin = 25
        trigger = Button(triggerPin, pull_up=False)
        # print(trigger) debut
        trigger.wait_for_press()
        # print("Button pressed!") #debug
        check_all()

        time.sleep(1)
        trigger.close()
        # t = t + 1 #debug
    except:
        # print(" Having trouble. Let's restart.")
        user_input = input(" Stop program (Return): ")
        break
