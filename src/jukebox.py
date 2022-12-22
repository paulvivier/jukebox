import json
import os
import sys
import sys
import time
from time import sleep
from pprint import pprint
import spotipy
import keypadSeeburg
import textwrap
import subprocess

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyPKCE

## Moved Done items to "Features" in README.md

## ------ Issues
##        Start loging issues here: 


def getMenuHeader():
    print(
        textwrap.dedent(
            """\
=========================================================================
    print(
        textwrap.dedent(
            """\
=========================================================================
 _______  _______  _______  ___      _______  _______  _______  _______ 
|       ||   _   ||  _    ||   |    |       ||       ||       ||       |
|_     _||  |_|  || |_|   ||   |    |    ___||_     _||   _   ||    _  |
  |   |  |       ||       ||   |    |   |___   |   |  |  | |  ||   |_| |
  |   |  |       ||  _   | |   |___ |    ___|  |   |  |  |_|  ||    ___|
  |   |  |   _   || |_|   ||       ||   |___   |   |  |       ||   |    
  |___|  |__| |__||_______||_______||_______|  |___|  |_______||___|    
     ___  __   __  ___   _  _______  _______  _______  __   __          
    |   ||  | |  ||   | | ||       ||  _    ||       ||  |_|  |         
    |   ||  | |  ||   |_| ||    ___|| |_|   ||   _   ||       |         
    |   ||  |_|  ||      _||   |___ |       ||  | |  ||       |         
 ___|   ||       ||     |_ |    ___||  _   | |  |_|  | |     |          
|       ||       ||    _  ||   |___ | |_|   ||       ||   _   |     ____        
|_______||_______||___| |_||_______||_______||_______||__| |__|     [Pv] 

=========================================================================    
 """
        )
    )


global device_id, pl_id, scope, sp_auth

# You'll need these ENVs in your shell. https://developer.spotify.com/
# SPOTIPY_CLIENT_ID=
# SPOTIPY_CLIENT_SECRET=
# SPOTIPY_REDIRECT_URI=

device_id = "98bb0735e28656bac098d927d410c3138a4b5bca"  # raspotify (raspberrypi)

# Default Playlist
### https://open.spotify.com/playlist/7D7FASC0bXRMdvfjggS0ug?si=05eae12ffb2b4b6b
pl_id = "6XIloMIjXr0QCQ8VdDPp7W"
offset = 0
scope = "user-read-playback-state,user-modify-playback-state,app-remote-control,streaming,playlist-modify-public"
# Authentication options. _May_ need to create a flow for reauthenticating.
# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp_auth = spotipy.Spotify(
    client_credentials_manager=SpotifyPKCE(scope=scope, open_browser=False)
)

# Directories to store API responses
dirName = [
    "cache"  # ,
    #'json/',
]


]


def make_some_dirs(dirName):
    for d in dirName:
        if not os.path.exists(d):
            os.mkdir(d)
            print("./", d, " Directory Created ")
        else:
            print("./", d, " Directory Found")



def init_lights():
    try:
        arg = ["raspi-gpio", "set", "27", "op", "dh"]
        turnon = subprocess.run(arg, capture_output=True)
        print(turnon.stdout, turnon.stderr)
        arg = ["raspi-gpio", "set", "23", "op", "dh"]
        turnon = subprocess.run(arg, capture_output=True)
        #print(turnon.stdout, turnon.stderr) # debug
        print("...Turned on initial lights")
    except:
        print("ERROR: Problem initializing lights")

def waitForKeys():
    print("Enter Song number with Keypad ")
    threeNumbers: str = ""

    while len(threeNumbers) < 3:
        # Loop until three digits have been entered on the keypad
        triggeredPins = keypadSeeburg.check_all()

        print(f"triggeredPins: {triggeredPins}")

        if triggeredPins != "ERR":
            # Add each new digit to the end of the string
            _ = pinsToDigits(triggeredPins[0], triggeredPins[1])
            threeNumbers += _
            print(f"threeNumbers: {threeNumbers}")
            if _ == "R":
                print("Reset !!!!")
                keypadSeeburg.menuLights(light="firstDigit", state="dl")
                keypadSeeburg.menuLights(light="secondDigit", state="dl")
                threeNumbers = ""
            elif len(threeNumbers) == 1:
                keypadSeeburg.menuLights(light="firstDigit", state="dh")
            elif len(threeNumbers) == 2:
                keypadSeeburg.menuLights(light="secondDigit", state="dh")

        else:
            print("Didnt get two pins")
            if len(threeNumbers) == 1:
                keypadSeeburg.menuLights(light="firstDigit", state="dh")
            elif len(threeNumbers) == 2:
                keypadSeeburg.menuLights(light="secondDigit", state="dh")

    print(f"I've got three digits! {threeNumbers}")


    songDigits = int(threeNumbers)  # Spotify Playlist Index starts at 0
    # track_selection = getSongID(songDigits)
    play_song(songDigits)
    print("Song played. Turn off lights")
    keypadSeeburg.menuLights(light="firstDigit", state="dl")
    keypadSeeburg.menuLights(light="secondDigit", state="dl")

# Loop through this until you get 3 digits from the keypad.
# Retrives LIVE playlist from Spotify and with desired fields
def list_playlist(pl_id) -> str:
    response = sp_auth.playlist_items(
        pl_id,
        offset=offset,
        fields="items.track.artists.name,items.track.name,items.track.id,total",
        additional_types=["track"],
    )
    if len(response["items"]) == 0:
        print("There are no items in your playlist.")

    return response


# Get's song details from a playlist.
def song_details(pl_id):
    response = list_playlist(pl_id)
    # response = sp.playlist_items(
    #     pl_id,
    #     offset=offset,
    #     fields="items.track.artists.name,items.track.name,items.track.id,total",
    #     additional_types=["track"],
    # )

    print(f"Current Playlist id: {pl_id}")
    playlist_track: int = int(
        input("Select playlist track # (index). Example: 0, 1, 2... : ")
    )
    if playlist_track >= len(response["items"]):
        print("---> Thre aren't that many songs on the playist. Try again. \n")
        return

    track_name = response["items"][playlist_track]["track"]["name"]
    track_id = response["items"][playlist_track]["track"]["id"]
    print(f"Playlist Index: {playlist_track}")
    print(f"Track Name: {track_name} -- Track ID: {track_id}")

    return track_id


def list_devices():
    # Services with personal info need authentication.
    print("\n************************** ")
    print(
        "Authenticating... \nIf presented with a URL, copy/paste to a browser, accept, and copy/paste final URL here. \n "
    )
    # sleep(1)
    res = sp_auth.devices()
    return res
    ## Responds with a list of Active devices


def play_song(track_selection):
    # Playing song by selecting position and context of the playlist
    # This will make the jukebox keep playing through the playlist.
    context_uri = f"spotify:playlist:{pl_id}"
    offset = {"position": track_selection}
    # print(f"context_uri = {context_uri}") #debug
    # print(f"offset = {offset}") #debug
    # print(f"device_id = {device_id}") #debug
    uris = None
    send = sp_auth.start_playback(device_id, context_uri, uris, offset)
    print(send)

    # TODO - Print name of device ID that you're playing on.


def store_local(json_data, file_prefix):
    file_name = file_prefix + ".json.cache"

    try:
        # json_data = requests.post(url, headers={'Authorization': 'Bearer ' + access_token}).json()
        with open(file_name, "w") as write_file:
            jsondump = json.dump(json_data, write_file, sort_keys=False, indent=4)
    except:
        print("Problem with making a connection.")

    with open(file_name, "r") as read_file:
        jsonload = json.load(read_file)

    print(jsonload)
    # Stores json respones locally for faster loading.
    return file_name


def setVolume(level):
    # Sets Spotify device to "soft" or "loud"

    if level == 1:
        sp_auth.volume(device_id=device_id, volume_percent=70)
    elif level == 0:
        sp_auth.volume(device_id=device_id, volume_percent=40)
    else:
        print("Error on setting")
    print(sp_auth.volume(device_id))


def keypadMatch(pinX, pinY):
    """
    Takes any two GPIO numbers, finds which digit on the keypad
    it matches to and returns that digit.

    """
    tic = time.perf_counter()
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
    # keypadPins = (
    # Needs updating
    #     (5, 7),  # 0
    #     (8, 17),  # 1
    #     (9, 12),  # 2
    #     (10, 13),  # 3
    #     (7, 10),  # 4
    #     (9, 10),  # 5
    #     (8, 10),  # 6
    #     (7, 8),  # 7
    #     (8, 9),  # 8
    #     (7, 9),  # 9
    #     (4, 4),  # Reset
    # )

    gpioToDigits = {
        0: (20, 16),  # 0
        1: (12, 5),  # 1
        2: (19, 13),  # 2
        3: (26, 6),  # 3
        4: (16, 26),  # 4
        5: (19, 26),  # 5
        6: (12, 26),  # 6
        7: (16, 12),  # 7
        8: (12, 19),  # 8
        9: (16, 19),  # 9
        "R": (21, 21),  # Reset
    }

    # Send the input pins (pinX & pinY) and see what KEYPAD NUMBERS match all of those pins.
    # Set pinX & pinY with pin values that are "HIGH" when side "click switch" is triggered

    # reset values to default
    keys = 0
    matchX: bool = False
    matchY: bool = False

    print(f"Checking match for pinX: {pinX} pinY: {pinY}")

    # Would like to rewrite this itterate automatically by the size of 'keys'
    # and then use that position in voltageKeys[keys]
    while keys < 11:
        # print(f"****** Checking on key: {keys}") #debug
        x = gpioToDigits[keys][0]
        y = gpioToDigits[keys][1]

        if pinX == x or pinY == x:
            print(f"Match on PinY or PinY: {x}")
            if pinX == x:
                matchX = True
            elif pinY == x:
                matchY = True
        elif pinX == x and pinY == x:
            matchX = True
            matchY = True

        if pinX == y or pinY == y:
            print(f"Match on PinY or PinY: {y}")
            if pinX == y:
                matchX = True
            elif pinY == y:
                matchY = True
        else:
            # print(f"-------[ Nothing Found Keypad: [{keys}] ") # debug
            matchX = False
            matchY = False

        if pinX == gpioToDigits["R"][0]:
            print("********** RESET button pushed!!  ********")
            matchX = True
            matchY = True
            keys = "R"
            return keys

        if matchX == True & matchY == True:
            print(f"==========-  Key {keys} was pressed ! -=========")
            toc = time.perf_counter()
            print(f"check_all() in {toc - tic:0.4f} seconds")
            return keys
        else:
            # increment keys
            keys = keys + 1

    return keys

# Python program to concatenate
# three numbers
def numConcat(num1, num2, num3):
    # Convert both the numbers to
    # strings
    num1 = str(num1)
    num2 = str(num2)
    num3 = str(num3)

    # Concatenate the strings
    num2 += num3
    num1 += num2

    return int(num1)


def getSongID(digits):

    # TODO: Read the cached json file instead of the API call
    response = list_playlist(pl_id)
    #   items.track.artists.name,
    #   items.track.name,
    #   items.track.id,total",
    #   additional_types=["track"],

    if digits >= 100 and digits < 289:  # and less than 289
        print(f"Jukebox number: {digits}")
        # modify 'digits' to map to a playlist index number
        # My jukebox labels start at 100 and go to 279, so we have a 0-179 song playlist
        digits = digits - 100

        # Using modified 'digits', send as index number of playlist
        track_name = response["items"][digits]["track"]["name"]
        track_id = response["items"][digits]["track"]["id"]
        print(f"Playlist Index: {digits}")
        print(f"Track Name: {track_name} -- Track ID: {track_id}")
        return track_id
    elif digits == 0:
        print("Special number: {digits}")
        if digits == 000:
            response = sp_auth.pause_playback(device_id)
            print(color.BOLD, color.RED + " * Playback Paused * " + color.END)
    elif digits >= 990:  # and less than or = to 999
        print("Special number: {digits}")
    else:
        print("ERROR: Selection not available.")


# This is the Menu of actions to do with various digits
def digitMenu(digits):

    if digits >= 100 and digits < 289:
        # Play a song
        track_selection = getSongID(digits)
        play_song(track_selection)
        print(
            color.BOLD,
            color.GREEN + "-> Playing Song -> : " + str(digits) + color.END,
        )
    elif digits < 100:
        print(
            color.BOLD,
            color.RED
            + "###### ERROR - Not a valid menu selection: "
            + str(digits)
            + color.END,
        )
    else:
        print(
            color.BOLD,
            color.RED
            + "###### ERROR - Not (yet) a valid menu selection: "
            + str(digits)
            + color.END,
        )


def pinsToDigits(pinX=0, pinY=0):
    """
    Send 'pinX' and 'pinY' to be mapped to a digit (optional)
    'manual' obtains pinX and pinY

    Responds with a single digit
    """
    keys = ""

    # Sends request to keypadMatch to map to digit and waits for a key.
    keypad = keypadMatch(pinX, pinY)
    keys = str(keypad)
    if keys is None:
        keys = "empty"
    print(f"Key pressed: {keys}")

    return keys


def set_repeat(state):
    """
    state - track, context, or off
    device_id - device target for playback
    """
    result = sp_auth.repeat(state, device_id)
    print(f"Results: {result}")


def search_spotify(search_artist=None, search_song=None):
    if search_artist == None:
        search_artist = input("Artist:")
        search_song = input("Song:")
    else:
        print(f"Artist: '{search_artist}' - Song: '{search_song}'")

    # sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    search_str = search_artist + "\t" + search_song
    result = sp_auth.search(search_str, limit=1)
    # pprint(result) #debug
    try:
        track_id = result["tracks"]["items"][0]["id"]
        track_name = result["tracks"]["items"][0]["name"]
        track_artist = result["tracks"]["items"][0]["album"]["artists"][0]["name"]
    except:
        track_id = "4cOdK2wGLETKBW3PvgPWqT"
        track_name = "No Results"
        track_artist = "No Results"
    print(f"{track_artist},{track_id},{track_name}")
    return track_artist, track_id, track_name


def makeplaylist():
    file_location = "../playlist/jukeboxplaylist.csv"
    print("CSV File format: artist, title: ")
    playlist_id = "6XIloMIjXr0QCQ8VdDPp7W"
    print("Default playlist ID: {playlist_id} ")
    import csv

    with open(file_location) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                search_artist = row[0]
                search_song = row[1]
                song_info = search_spotify(search_artist, search_song)
                id = [str(song_info[1])]  # playlist_add_items requies a list
                # print(f"id: {id}")
                print(sp_auth.playlist_add_items(playlist_id, id))
                sleep(2)
                # input("(Return) to Continue")  # break to debug

                line_count += 1
        list_playlist(playlist_id)

# print(color.BOLD + 'Hello World !' + color.END)
# https://stackoverflow.com/questions/8924173/how-to-print-bold-text-in-python
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


# Let's start this puppy up. 
while True:
    print(color.BOLD + "\n **** Spotify CLI Commands  ****" + color.END)
    print(color.BOLD + "0" + color.END + " - Exit the console")
    print(color.BOLD + "1" + color.END + " - Set Playlist for Session")
    print(color.BOLD + "2" + color.END + " - List Song ID from Playlist")
    print(color.BOLD + "3" + color.END + " - Play song by playlist position")
    print(color.BOLD + "4" + color.END + " - Set Device")
    print(color.BOLD + "5" + color.END + " - Pause Playback")
    print(color.BOLD + "6" + color.END + " - Resume Playback")
    print(color.BOLD + "7" + color.END + " - Save Playlist Locally")
    print(
        color.BOLD
        + "8"
        + color.END
        + " - "
        + color.GREEN
        + "Select song with keypad"
        + color.END
    )
    print(color.BOLD + "9" + color.END + " - Search for Song ")
    print(
        color.BOLD
        + "10"
        + color.END
        + " - Make Playlist from CSV (only need Artist,Title) "
    )
    print(color.BOLD + "11" + color.END + " - Turn Lights On ")
    print(color.BOLD + "12" + color.END + " - Turn Lights Off ")
    print(color.BOLD + "13" + color.END + " - Test loud/quiet button")
    print(color.BOLD + "14" + color.END + " - Initialize starting lights")
    print(color.BOLD + "15" + color.END + " - Test valid number entries")
    print(color.BOLD + "16" + color.END + " - Set Song Repeat state")
    print(color.BOLD + "17" + color.END + " - Check Keypad pinouts")
    user_input = int(input(color.BOLD + "Enter Your Choice: " + color.END))

def menuCommands(user_input, device_id, pl_id):
    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")

    # Set New Playlist
    elif user_input == 1:
        # Post Breakup - Dumped: 6LcIWHYEZPyjx3nqdzDhuL
        pl_id = input("Enter New Playlist ID:")
        print(f"New Playlist ID has been changed to {pl_id}")

    elif user_input == 2:
        song_details(pl_id)
        # track_id = ()

    # Play Song By ID
    elif user_input == 3:

        track_selection = str(input("Enter Track position on playlist: "))
        play_song(track_selection)
        print(
            color.BOLD,
            color.GREEN + "-> Playing Song -> : " + track_selection + color.END,
        )

    elif user_input == 4:
        # Shows devices that can be played on
        pprint(list_devices())
        device_id = input("Enter new device ID:")

    elif user_input == 5:
        # Pauses playback
        response = sp_auth.pause_playback(device_id)
        print(color.BOLD, color.RED + " * Playback Paused * " + color.END)

    elif user_input == 6:
        # Restart Paused Playback
        response = sp_auth.start_playback(device_id)
        print(color.BOLD, color.GREEN + " > Playback Resumed > " + color.END)

    elif user_input == 7:
        # Saves Playlist Locally
        response = list_playlist(pl_id)
        file_prefix = "cache/playlist_" + pl_id
        file_name: str = store_local(response, file_prefix)
        print(
            color.BOLD,
            color.GREEN + " # Stored Playlist locally #: " + file_name + color.END,
        )

    elif user_input == 8:
        print("Enter Song number with Keypad ")
        threeNumbers: str = ""

        while len(threeNumbers) < 3:
            # Loop until three digits have been entered on the keypad
            triggeredPins = keypadSeeburg.check_all()

            print(f"triggeredPins: {triggeredPins}")

            if triggeredPins != "ERR":
                # Add each new digit to the end of the string
                _ = pinsToDigits(triggeredPins[0], triggeredPins[1])
                threeNumbers += _
                print(f"threeNumbers: {threeNumbers}")
                if len(threeNumbers) == 1:
                    keypadSeeburg.menuLights(light="firstDigit", state="dh")
                elif len(threeNumbers) == 2:
                    keypadSeeburg.menuLights(light="secondDigit", state="dh")

            else:
                print("Didnt get two pins")
                if len(threeNumbers) == 1:
                    keypadSeeburg.menuLights(light="firstDigit", state="dh")
                elif len(threeNumbers) == 2:
                    keypadSeeburg.menuLights(light="secondDigit", state="dh")

        print(f"I've got three digits! {threeNumbers}")

        # [Debug] - Swap this out with the shorter section below to be able to decline.
        # userChoicePlay = str(
        #     input(f"Would you like to play song # {threeNumbers} on the playlist?(Y/N)")
        # )
        # songDigits = int(threeNumbers)  # Spotify Playlist Index starts at 0
        # if userChoicePlay == "Y":
        #     track_selection = getSongID(songDigits)
        #     play_song(track_selection)
        # else:
        #     print("Canceling song selection")

        songDigits = int(threeNumbers)  # Spotify Playlist Index starts at 0
        # track_selection = getSongID(songDigits)
        play_song(songDigits)
        print("Song played. Turn off lights")
        keypadSeeburg.menuLights(light="firstDigit", state="dl")
        keypadSeeburg.menuLights(light="secondDigit", state="dl")

    # Loop through this until you get 3 digits from the keypad.
    elif user_input == 9:
        search_spotify()

    elif user_input == 10:
        makeplaylist()

    elif user_input == 11:
        # print("Cycling through display lights.")

        choice = input(
            "1] Reset\n2] Coin\n3] 1st Digit\n4] Single \n5] 2nd Digit\n6] Album\n7] Dash\n8] Test All \n: "
        )

        if choice == "1":
            keypadSeeburg.menuLights(light="reset", state="dh")
        elif choice == "2":
            keypadSeeburg.menuLights(light="depositCoins", state="dh")
        elif choice == "3":
            keypadSeeburg.menuLights(light="firstDigit", state="dh")
        elif choice == "4":
            keypadSeeburg.menuLights(light="selectSingle", state="dh")
        elif choice == "5":
            keypadSeeburg.menuLights(light="secondDigit", state="dh")
        elif choice == "6":
            keypadSeeburg.menuLights(light="selectAlbumn", state="dh")
        elif choice == "7":
            keypadSeeburg.menuLights(light="dashLights", state="dh")
        elif choice == "8":
            keypadSeeburg.menuLights(light="", test=True, state="")

    elif user_input == 12:
        # print("Turn Lights Off.")

        choice = input(
            "1] Reset\n2] Coin\n3] 1st Digit\n4] Single \n5] 2nd Digit\n6] Album\n7] Dash\n8] Test All \n: "
        )

        if choice == "1":
            keypadSeeburg.menuLights(light="reset", state="dl")
        elif choice == "2":
            keypadSeeburg.menuLights(light="depositCoins", state="dl")
        elif choice == "3":
            keypadSeeburg.menuLights(light="firstDigit", state="dl")
        elif choice == "4":
            keypadSeeburg.menuLights(light="selectSingle", state="dl")
        elif choice == "5":
            keypadSeeburg.menuLights(light="secondDigit", state="dl")
        elif choice == "6":
            keypadSeeburg.menuLights(light="selectAlbumn", state="dl")
        elif choice == "7":
            keypadSeeburg.menuLights(light="dashLights", state="dl")
        elif choice == "8":
            keypadSeeburg.menuLights(light="", test=True, state="")

    elif user_input == 13:
        if keypadSeeburg.checkLoud() == True:
            setVolume(level=1)
        else:
            setVolume(level=0)

    elif user_input == 14:
        init_lights()

    elif user_input == 15:
        _ = int(input("Enter Digits to test: "))
        digitMenu(_)

    elif user_input == 16:
        _ = input("Enter one of the following: 'track', 'context', or 'off': ")
        print(f"Setting to {_}")
        set_repeat(_)

    elif user_input == 17:
        loop = 0
        while loop < 5:
            try:
                triggeredPins = keypadSeeburg.check_all()
                pinsToDigits(triggeredPins[0], triggeredPins[1])
                loop = loop + 1
                print(f"Loop #{loop}")
            except:
                print("Error: Problem with getting pins or mapping to digit")
    else:

        print("Please enter valid user-input.")
