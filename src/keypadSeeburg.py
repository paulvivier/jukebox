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

### Pins triggered in pairs without voltage pins
voltageKeys = {
    0: (5, 7),  # 0
    1: (8, 17),  # 1
    2: (9, 12),  # 2
    3: (10, 13),  # 3
    4: (7, 10),  # 4
    5: (9, 10),  # 5
    6: (8, 10),  # 6
    7: (7, 8),  # 7
    8: (8, 9),  # 8
    9: (7, 9),  # 9
    "R": (4, 4),  # Reset
}

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
    """
    Get the gpio addresses for two pins once the triggered
    switch/pin has been activated.
    """
    setPins()
    print("### Press buttons slowly. Wait for Attempt to itterate ")
    gpio1 = 0
    gpio2 = 0
    triggerPin = 25
    faulthandler.enable()
    trigger = Button(triggerPin, pull_up=False)
    # print(trigger) debut
    trigger.wait_for_press()
    # print("Button pressed!") #debug
    for x in keyPins.keys():  # itterates through the keys (keyboard pins)
        gpio = keyPins[x]
        button = Button(gpio, pull_up=False)
        # print(f"{x},", end="")
        # print(f"Checking key:{x} gpio:{gpio}", end="")  # debug
        # print(button.is_pressed)
        if button.value:
            print(f"Activated: keyPadPinout:{x} - gpio:{gpio}")
            if gpio1 > 0:
                gpio2 = gpio
                button.close()
            else:
                gpio1 = gpio
                button.close()
            if gpio2 > 0:

                print("return 1")
                time.sleep(1)
                return gpio1, gpio2

    print("_______________________")
    # print("Repeat")
    trigger.close()
    time.sleep(1)
    print("<ERROR> - Didn't get two pins.")
    message = "ERR"
    return message

    # while True:
    #     try:
    #         triggeredPins = check_all()
    #         print(f"triggeredPins: {triggeredPins}")
    #         # Get voltageKeys key for matching triggeredPins
    #     except:
    #         user_input = input(
    #             "________________________\nStopping program. Fault triggered: (RETURN)"
    #         )
    #         break
