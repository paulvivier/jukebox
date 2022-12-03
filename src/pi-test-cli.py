#!/usr/bin/python3

from gpiozero import LED, Button
from signal import pause


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# print(color.BOLD + 'Hello World !' + color.END)
# https://stackoverflow.com/questions/8924173/how-to-print-bold-text-in-python


while True:
    print(color.BOLD + "\n **** Spotify CLI Commands  ****" + color.END)
    print(color.BOLD + "0" + color.END + " - Exit the CLI")
    print(color.BOLD + "1" + color.END + " - Button Pinout Test")
    print(color.BOLD + "2" + color.END + " -")
    print(color.BOLD + "3" + color.END + " - ")
    print(color.BOLD + "4" + color.END + " - ")
    print(color.BOLD + "5" + color.END + " - ")
    print(color.BOLD + "6" + color.END + " - ")
    print(color.BOLD + "7" + color.END + " - ")
    print(color.BOLD + "8" + color.END + " - ")
    user_input = int(input(color.BOLD + "Enter Your Choice: " + color.END))

    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")
        break

    # Blink Light, take input
    elif user_input == 1:

        print("#### Press Keypad buttons to light LED on Pi")

        keyPins = {
            # keyboard pin : gpio pin
            4: 21,
            5: 20,
            7: 8,
            8: 12,
            9: 26,
            10: 19,
            12: 13,
            13: 6,
            17: 5,
        }
        # led = 17

        while True:
            print("true")
            for x in keyPins.keys():  # itterates through the keys (keyboard pins)
                gpio = keyPins[x]
                button = Button(gpio)
                print(f"key:{x} -> gpio:{button}")  # debug
                if button.is_active:
                    print(f"GPIO {gpio} is active")
                else:
                    print(f"No value for GPIO:{x}")

    else:
        print("Please enter valid user-input.")
