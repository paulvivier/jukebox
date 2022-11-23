# from fileinput import filename
# from sys import breakpointhook
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep
import json


##  TODO
##  Fix oAuth flow (DONE!)
##  Make menus into functions. (DONE!)
##  Start play on device from playlist index selection
##  Specify new global device id.
##  Save more JSON locally for reference. Require at 'setup'. Remove ids from code.
##  Map Numbers 100 - 279 to playlist index


path = "/Applications/Spotify.app"

# You'll need these ENVs in your shell. https://developer.spotify.com/
# SPOTIPY_CLIENT_ID=
# SPOTIPY_CLIENT_SECRET=
# SPOTIPY_REDIRECT_URI=


# Device options until you can add ability to specify a different one.
device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"  # laptop
# device_id = "78776d6cc7f769f4ea5e302aa41977e9211af158"  # phone

# Default Playlist
### https://open.spotify.com/playlist/7D7FASC0bXRMdvfjggS0ug?si=05eae12ffb2b4b6b
pl_id = "7D7FASC0bXRMdvfjggS0ug"
offset = 0


scope = (
    "user-read-playback-state,user-modify-playback-state,app-remote-control,streaming"
)
# Authentication options. _May_ need to create a flow for reauthenticating.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp_auth = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))


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

    # pprint(f"Items in Playlist: {response['items']}")

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
        print("---> Selection is longer than list\n")
        return

    track_name = response["items"][playlist_track]["track"]["name"]
    track_id = response["items"][playlist_track]["track"]["id"]
    print(f"Playlist Index: {playlist_track}")
    pprint(f"Track Name: {track_name} -- Track ID: {track_id}")


def list_devices():
    # Personal info needs reauthorizing so needs to go through OAuth.

    # TODO - Fancy If statment to check expiration on oauth session and NOT display this message.
    print("\n************************** ")
    print(
        "You are going to be redirected to your browser. \nCopy the URL and come back to this screen \n "
    )
    sleep(5)
    res = sp_auth.devices()
    return res
    ## Responds with a list of Active devices


def play_song(track_selection):
    # playback_uris: list[str] = ["spotify:track:6exdwZ3EOSCjb11bd6k6Np"]

    # Transform input into list
    new_track = f"spotify:track:{track_selection}"
    playback_uris = [new_track]

    # Open Spotify App locally. Small delay so API can see it.
    # Comment out for faster testing during development
    # os.system(f"open {path}")
    # sleep(5)

    # TODO - Print name of device ID that you're playing on.

    pprint(sp_auth.start_playback(device_id, uris=playback_uris))
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


# keypad diagnostics
# Press a number on a keypad and print the pins triggered.
def keypadMatch():
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
    voltageKeys = (
        (5, 7),  # 0
        (8, 17),  # 1
        (9, 12),  # 2
        (10, 13),  # 3
        (7, 10),  # 4
        (9, 10),  # 5
        (8, 10),  # 6
        (7, 8),  # 7
        (8, 9),  # 8
        (7, 9),  # 9
        (4, 4),  # Reset
    )
    # When the big 'click' happens, read the input pins.

    # Store the input pins and see what NUMBERS match all of those pins.
    # start by taking usr input and looking up the values to see if there are any matches.
    # Set pinX & pinY with pin values that are "HIGH" when side "click switch" is triggered
    pinX = 0
    pinY = 0
    print("Enter value of first pin triggered:")
    pinX = int(input())
    print("Enter value of second pin triggered:")
    pinY = int(input())

    # reset values to default
    keys = 0
    matchX: bool = False
    matchY: bool = False

    # Would like to rewrite this itterate automatically by the size of 'keys'
    # and then use that position in voltageKeys[keys]
    while keys < 11:
        print(f"****** Checking on key: {keys}")
        print(f"Checking match for pinX: {pinX} pinY: {pinY}")

        x = voltageKeys[keys][0]
        y = voltageKeys[keys][1]
        print(f"Value expected for X for keypad {keys}: {x}")
        print(f"Value expected for Y for keypad {keys}: {y}")

        if pinX == x or pinY == x:
            print(f"Match on PinY or PinY: {x}")
            if pinX == x:
                matchX = True
            elif pinY == x:
                matchY = True
        else:
            print("Nothing")

        if pinX == y or pinY == y:
            print(f"Match on PinY or PinY: {y}")
            if pinX == y:
                matchX = True
            elif pinY == y:
                matchY = True
        else:
            print(f"Nothing Found Keypad: [{keys}] ")
            matchX = False
            matchY = False

        if pinX == 4 or pinY == 4:
            print("********** Time for a RESET, baby ********")
            matchX = True
            matchY = True
            keys = 11

        if matchX == True & matchY == True:
            print(f"********* Matchy Match on Keypad: [{keys}] **************")
            break
        else:
            print("No matches")
            keys = keys + 1

    return


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


while True:
    print(color.BOLD + "\n **** Spotify CLI Commands  ****" + color.END)
    print(color.BOLD + "0" + color.END + " - Exit the console")
    print(color.BOLD + "1" + color.END + " - Set Playlist for Session")
    print(color.BOLD + "2" + color.END + " - List Song on Playlist")
    print(color.BOLD + "3" + color.END + " - Play song by ID")
    print(color.BOLD + "4" + color.END + " - List Devices")
    print(color.BOLD + "5" + color.END + " - Pause Playback")
    print(color.BOLD + "6" + color.END + " - Resume Playback")
    print(color.BOLD + "7" + color.END + " - Save Playlist Locally")
    print(color.BOLD + "8" + color.END + " - Reset System")
    print(color.RED + "9" + color.END + " - [Testing] Keypad entry ")
    user_input = int(input(color.BOLD + "Enter Your Choice: " + color.END))

    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")
        break

    # Update/Display Playlist
    elif user_input == 1:
        # Check locally for playlist first and display.
        cache_files = os.listdir("cache")
        cache_files.remove(".DS_Store")  # get rid of Macos junk
        print(f"Files in Cache: {cache_files}")

        ### Open cache file by Index #
        ### Just checking to make sure the contents look right
        cache_files[0] = "cache/" + cache_files[0]  # add cache/ directory prefix
        with open(cache_files[0], "r") as read_file:
            jsonload = json.load(read_file)
        print(jsonload)

        # Prompt - Use Local or Live playlist?
        # Post Breakup - Dumped: 6LcIWHYEZPyjx3nqdzDhuL
        user_input2 = input("Set new playlist for session (and save locally?) Y/N:")
        if user_input2 == "Y":
            pl_id = input("Enter Playlist ID:")
            response = list_playlist(pl_id)
            pprint(f"Playlist: {response}")
            file_prefix = "cache/playlist_" + pl_id
            file_name2: str = store_local(response, file_prefix)
            print(
                color.BOLD,
                color.GREEN + " # Stored Playlist locally #: " + file_name2 + color.END,
            )
            print(f"New Playlist ID has been changed to {pl_id}")

        else:
            print()

    elif user_input == 2:
        song_details(pl_id)

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

        print("Reset System")
        # Dowload copy of default playlist at bootup. Default is set in code.
        # Specify another playlist as default while using the app
        # Dowload copy of new default playlist

    elif user_input == 9:

        keypadMatch()

    else:

        print("Please enter valid user-input.")
