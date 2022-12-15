import json
import os
from time import sleep
from pprint import pprint
import spotipy
import keypadSeeburg
import textwrap

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyPKCE

##  TODO
##  (DONE!) Fix oAuth flow 
##  (DONE!) Refactored authentication flow to work headlesss. Converted to PKCE 
##  (DONE!) Refactor: Make menus into functions. 
##  (DONE!) Start play on device from playlist index selection 
##  (DONE!) Map pins on keypad to GPIO on raspberry pi to produce a number 
##  (DONE!) Merge changes from raspberry pi 
##  (DONE!) Install Raspotify (https://pimylifeup.com/raspberry-pi-spotify/) 
##                    (Done!)(https://github.com/dtcooper/raspotify/wiki/Basic-Setup-Guide) 
##  (Done!) Establish better thread management of on GPIO checking to prevent Segmentation Faults 
##  (Done!) Map Numbers 100 - 279 to playlist index 
##  (Done!) Create (automate?) full playlist (Menue #10)
##  - Add song to Queue instead of play immediate. (keep playing current song)
##  - Set up secret number library: 1) Force song to play 2) shutdown
##  - Trigger lights to acknowledge key reciept. (6 lights)
##  - Fix Reset button . Note that Reset can use a secondary pin. (Light?)
##  - Add Volume Buttons
##  - Add Power monitoring to Pi. 
## ------ Hardware 
##  (DONE!) Solder board for menu lights
##  (DONE!) Consolidate wiring to fit in jukebox. Retest. Fix Bugs 
##  (DONE!) Get rid of hum in amplifyer. (used a better power supply)
##  - Determine how to power LEDS for rest of box. 
## ------ Nice to have ---
##  Dowload copy of default playlist at bootup. Default is set in code.
##  Specify another playlist as default while using the app
##  Dowload copy of new default playlist
##  Specify new global device id.
##  Save more JSON locally for reference. Require at 'setup'. Remove ids from code.
## ------ Not going to do
##  (No) Display number selected. 

def getMenuHeader():
    print(textwrap.dedent("""\
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
|       ||       ||    _  ||   |___ | |_|   ||       ||   _   |         
|_______||_______||___| |_||_______||_______||_______||__| |__|  
    
=========================================================================    
 """))


path = "/Applications/Spotify.app"

# You'll need these ENVs in your shell. https://developer.spotify.com/
# SPOTIPY_CLIENT_ID=
# SPOTIPY_CLIENT_SECRET=
# SPOTIPY_REDIRECT_URI=


# Device options until you can add ability to specify a different one.
# device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"  # laptop
# device_id = "78776d6cc7f769f4ea5e302aa41977e9211af158"  # phone
device_id = "98bb0735e28656bac098d927d410c3138a4b5bca"  # raspotify (raspberrypi)


# Default Playlist
### https://open.spotify.com/playlist/7D7FASC0bXRMdvfjggS0ug?si=05eae12ffb2b4b6b
pl_id = "6XIloMIjXr0QCQ8VdDPp7W"
offset = 0


scope = "user-read-playback-state,user-modify-playback-state,app-remote-control,streaming,playlist-modify-public"
# Authentication options. _May_ need to create a flow for reauthenticating.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# OAUTH
# sp_auth = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# PKCE
# Requires a more detailed browser authorization.
# Produces a
sp_auth = spotipy.Spotify(
    client_credentials_manager=SpotifyPKCE(scope=scope, open_browser=False)
)

# Directories to store API responses
dirName = [
    "cache"  # ,
    #'json/',
    ]
def make_some_dirs(dirName):
    for d in dirName:
        if not os.path.exists(d):
            os.mkdir(d)
            print("./", d, " Directory Created ")
        else:
            print("./", d, " Directory Found")


# Retrives LIVE playlist from Spotify and with desired fields
def list_playlist(pl_id) -> str:
    response = sp.playlist_items(
        pl_id,
        offset=offset,
        fields="items.track.artists.name,items.track.name,items.track.id,total",
        additional_types=["track"],
    )
    if len(response["items"]) == 0:
        print("There are no items in your playlist.")

    ### print("Items in Response:")
    ### {'track': {'artists': [{'name': 'New Order'}],
    ###           'id': '1RSy7B2vfPi84N80QJ6frX',
    ###           'name': 'Blue Monday - 2016 Remaster'}}

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
    # playback_uris: list[str] = ["spotify:track:6exdwZ3EOSCjb11bd6k6Np"]

    # Transform input into list
    new_track = f"spotify:track:{track_selection}"
    print(f"New Track URI: {new_track}")
    playback_uri = new_track
    playback_uris = [new_track]

    # Open Spotify App locally. Small delay so API can see it.
    # Comment out for faster testing during development
    # os.system(f"open {path}")
    # sleep(5)

    # TODO - Print name of device ID that you're playing on.

    #print(sp_auth.add_to_queue(uri=playback_uri))
    print(sp_auth.start_playback(device_id, uris=playback_uris))
            # start_playback PARMS:
            # start_playback(
            #       device_id=None,
            #       context_uri=None,
            #       uris=None,
            #       offset=None,
            #       position_ms=None
            # )


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


def keypadMatch(pinX, pinY):
    """
    Takes any two GPIO numbers, finds which digit on the keypad
    it matches to and returns that digit.

    """
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
        print(f"****** Checking on key: {keys}")
        x = gpioToDigits[keys][0]
        y = gpioToDigits[keys][1]

        if pinX == x or pinY == x:
            print(f"Match on PinY or PinY: {x}")
            if pinX == x:
                matchX = True
            elif pinY == x:
                matchY = True

        if pinX == y or pinY == y:
            print(f"Match on PinY or PinY: {y}")
            if pinX == y:
                matchX = True
            elif pinY == y:
                matchY = True

        else:
            print(f"-------[ Nothing Found Keypad: [{keys}] ")
            matchX = False
            matchY = False

        if pinX == 4 or pinY == 4:
            print("********** RESET button pushed!!  ********")
            matchX = True
            matchY = True
            keys = 11
            return keys

        if matchX == True & matchY == True:
            print(f"==========-  Key {keys} was pressed ! -=========")
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

    if digits >= 100:  # and less than 289
        print("Jukebox number: {digits}")
        # modify 'digits' to map to a playlist index number
        # My jukebox labels start at 100 and go to 279, so we have a 0-179 song playlist
        digits = digits - 100

        # Using modified 'digits', send as index number of playlist
        track_name = response["items"][digits]["track"]["name"]
        track_id = response["items"][digits]["track"]["id"]
        print(f"Playlist Index: {digits}")
        print(f"Track Name: {track_name} -- Track ID: {track_id}")
        return track_id
    elif digits >= 990:  # and less than or = to 999
        print("Special number: {digits}")
    else:
        print("ERROR: Selection not available.")


# This is the Menu of actions to do with various digits
def digitMenu(digits):

    if digits >= 100 & digits < 180:
        # Play a song
        track_selection = getSongID(digits)
        play_song(track_selection)
        print(
            color.BOLD,
            color.GREEN + "-> Playing Song -> : " + digits + color.END,
        )
    elif digits < 100:
        print(
            color.BOLD,
            color.RED
            + "###### ERROR - Not a valid menu selection: "
            + digits
            + color.END,
        )
    else:
        print(
            color.BOLD,
            color.RED
            + "###### ERROR - Not (yet) a valid menu selection: "
            + digits
            + color.END,
        )


def pinsToDigits(pinX=0, pinY=0):
    """
    Send 'pinX' and 'pinY' to be mapped to a digit (optional)
    'manual' obtains pinX and pinY

    Responds with three digits that map to a song number.
    """
    keys = ""

    # Sends request to keypadMatch to map to digit and waits for a key.
    pair = keypadMatch(pinX, pinY)
    keys = str(pair)
    if keys is None:
        keys = "empty"
    print(f"Key pressed: {keys}")

    return keys


def search_spotify(search_artist=None, search_song=None):
    if search_artist == None:
        search_artist = input("Artist:")
        search_song = input("Song:")
    else:
        print(f"Artist: '{search_artist}' - Song: '{search_song}'")

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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


# -----------------------------
# Print Header
getMenuHeader()
# -----------------------------
# Initialize directories
make_some_dirs(dirName)
# -----------------------------
# Let's start this puppy up. 
while True:
    print(color.BOLD + "\n **** Spotify CLI Commands  ****" + color.END)
    print(color.BOLD + "0" + color.END + " - Exit the console")
    print(color.BOLD + "1" + color.END + " - Set Playlist for Session")
    print(color.BOLD + "2" + color.END + " - List Song ID from Playlist")
    print(color.BOLD + "3" + color.END + " - Play song by ID")
    print(color.BOLD + "4" + color.END + " - Set Device")
    print(color.BOLD + "5" + color.END + " - Pause Playback")
    print(color.BOLD + "6" + color.END + " - Resume Playback")
    print(color.BOLD + "7" + color.END + " - Save Playlist Locally")
    print(color.BOLD + "8" + color.END + " - " + color.GREEN + "Use keypad" + color.END)
    print(color.BOLD + "9" + color.END + " - Search for Song ")
    print(color.BOLD + "10" + color.END + " - Make Playlist from CSV ")
    print(color.BOLD + "11" + color.END + " - Cycle through menu lights ")
    user_input = int(input(color.BOLD + "Enter Your Choice: " + color.END))

    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")
        break

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

        track_selection = str(input("Enter Track ID: "))
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
        response = sp.pause_playback(device_id)
        print(color.BOLD, color.RED + " * Playback Paused * " + color.END)

    elif user_input == 6:
        # Restart Paused Playback
        response = sp.start_playback(device_id)
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
        print("Test Keypad - refactor")
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
                    keypadSeeburg.menuLights(light="firstDigit")
                elif len(threeNumbers) == 2:
                    keypadSeeburg.menuLights(light="secondDigit")

            else:
                print("Didnt get two pins")
                if len(threeNumbers) == 1:
                    keypadSeeburg.menuLights(light="firstDigit")
                elif len(threeNumbers) == 2:
                    keypadSeeburg.menuLights(light="secondDigit")

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
        track_selection = getSongID(songDigits)
        play_song(track_selection)




    # Loop through this until you get 3 digits from the keypad.
    elif user_input == 9:
        search_spotify()

    elif user_input == 10:
        makeplaylist()

    elif user_input == 11:
        #print("Cycling through display lights.")
        
        choice = input("1] Reset\n2] Coin\n3] 1st Digit\n4] Single \n5] 2nd Digit\n6] Album\n7] Test All \n: ")
        
        if choice == "1":
            keypadSeeburg.menuLights(light="reset")
        elif choice == "2":
            keypadSeeburg.menuLights(light="depositCoins")
        elif choice == "3":
            keypadSeeburg.menuLights(light="firstDigit")
        elif choice == "4":
            keypadSeeburg.menuLights(light="selectSingle")
        elif choice == "5":
            keypadSeeburg.menuLights(light="secondDigit")
        elif choice == "6":
            keypadSeeburg.menuLights(light="selectAlbumn")
        elif choice == "7":
            keypadSeeburg.menuLights(light="", test=True)

    else:

        print("Please enter valid user-input.")
