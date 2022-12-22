import faulthandler
from gpiozero import Button, LED
import time
import subprocess


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
# troubleshooting problem with
#  #2 - Triggering gpio 19 & not gpio 13 from keypadPin 9 & 12
#  #R - Not triggering anything - should be triggering gpio 21


keyPins = {
    # keyboard pin : gpio pin
    # 3v to these keyboard pins : 1,2,3,6,11,14,15,16
    4: 21,
    5: 20,
    7: 16,
    8: 12,
    9: 19,
    10: 26,
    12: 13,
    13: 6,
    17: 5,
}

lightPins = {
    "reset": 17,  # Reset and ReSelect
    "depositCoins": 27,  # Deposit more coins
    "firstDigit": 9,  # 1st Digit
    "selectSingle": 10,  # Select any Single
    "secondDigit": 11,  # 2nd Digit
    "selectAlbumn": 22,  # Select any Albumn
    "dashLights": 23,  # dashLights
}


def checkLoud(gpio=24):  # checks the state of the button
    # GPIO 24 for "Loud" volume button
    volume_loud = Button(gpio, pull_up=True)

    print(f"volume_loud: {volume_loud}")
    if volume_loud.is_pressed == 1:
        print(f"LOUD!! volume_loud: {volume_loud} ")
        volume_loud.close()
        return True
    if volume_loud.is_pressed == 0:
        print(f"_soft_(shhh!) volume_loud: {volume_loud} ")
        volume_loud.close()
        return False


def menuLights(light, state, test=False):
    """
    Takes a key value of lightPins{} as _light_ parameter and
    turns it on. Will also test blinking all lights if test=TRUE and lights=""
    state = dh|dl (output or input), ""

    """

    if test == True:
        turns = 0
        while turns < 10:
            for x in lightPins.keys():
                gpio = lightPins[x]
                # print(f"gpio: {gpio}") #debug
                led = LED(gpio)
                led.on()
                time.sleep(0.08)
                led.off()
            turns = turns + 1

    elif len(state) == 2:
        gpio = lightPins[light]
        # print(f"gpio: {gpio}")
        gpio_str = str(gpio)
        # print(f"gpio_str: {gpio_str}")
        # led.on()
        arg = ["raspi-gpio", "set", "op"]
        arg.insert(2, gpio_str)
        arg.insert(5, state)
        print(arg)
        ## arg should look like = ["raspi-gpio", "set", led, "op", "dh"]
        ## raspi-gpio is faster and enables the light to stay on past gpio threads.
        ## apparently more dangerous too so ... who knows what I'll mess up.
        setLed = subprocess.run(arg, capture_output=True)
        print(setLed.stdout, setLed.stderr)
        # time.sleep(5)
        print(f"gpio {gpio_str} was set to {state} ")


def setPins(whichPins):
    print("Setting Pin defaults")
    for x in whichPins.keys():
        gpio = whichPins[x]
        Button(gpio, pull_up=False)


def quickcheck_all():
    """
    Get the gpio addresses for two pins once the triggered
    switch/pin has been activated.
    """
    setPins(keyPins)
    print("### Press buttons slowly. Wait for Attempt to itterate ")
    gpios = []
    triggerPin = 25
    #    faulthandler.enable()
    trigger = Button(triggerPin, pull_up=False)
    # print(trigger) debut
    trigger.wait_for_press()
    tic = time.perf_counter()
    # print("Button pressed!") #debug
    for x in keyPins.keys():  # itterates through the keys (keyboard pins)
        gpio = keyPins[x]
        print(f"gpio: {gpio}")
        print(f"gpios: {gpios}")
        button = Button(gpio, pull_up=False)
        if button.value == 1:
            gpios.append(gpio)
            button.close()
            continue
        if len(gpios) == 2:
            print("Returning gpios: {gpios}")
            return gpios


def check_all():
    """
    Get the gpio addresses for two pins once the triggered
    switch/pin has been activated.
    """
    setPins(keyPins)
    print("### Press buttons slowly. Wait for Attempt to itterate ")
    gpio1 = 0
    gpio2 = 0
    triggerPin = 25
    #    faulthandler.enable()
    trigger = Button(triggerPin, pull_up=False)
    # print(trigger) debut
    trigger.wait_for_press()
    tic = time.perf_counter()
    # print("Button pressed!") #debug
    for x in keyPins.keys():  # itterates through the keys (keyboard pins)
        gpio = keyPins[x]
        button = Button(gpio, pull_up=False)
        if button.value:
            print(f"Activated: keyPadPinout:{x} - gpio:{gpio}")

            if gpio1 > 0:
                button2 = button
                gpio2 = gpio
                button2.close()
            else:
                button1 = button
                gpio1 = gpio
                button1.close()
                trigger.close()
                if x == 4:
                    gpio2 = gpio
            if gpio2 > 0:
                time.sleep(1)
                toc = time.perf_counter()
                print(f"check_all() in {toc - tic:0.4f} seconds")
                return gpio1, gpio2

    print("_______________________")
    # print("Repeat")

    # time.sleep(1)
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
