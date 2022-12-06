from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep
import json


# Set defaults
path = "/Applications/Spotify.app"

# You'll need these ENVs in your shell. https://developer.spotify.com/
# SPOTIPY_CLIENT_ID=
# SPOTIPY_CLIENT_SECRET=
# SPOTIPY_REDIRECT_URI=


# Default Devices - need to move these to cached json.
device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"  # laptop
# device_id = "78776d6cc7f769f4ea5e302aa41977e9211af158"  # phone

# Default Playlist ID
pl_id = "7D7FASC0bXRMdvfjggS0ug"  # "Tabletop Jukebox playlist"


# -----------------------------------------------------------------------
# Setup calls to SpotiFy API using spotiPy.
# OAuth calls will expire an hour after authentication. Others will not.
scope = (
    "user-read-playback-state,user-modify-playback-state,app-remote-control,streaming"
)
# Authentication options. _May_ need to create a flow for reauthenticating.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp_auth = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# used in plalist_items - Not sure what it's doing TBH
offset = 0


# -----------------------------------------------------------------------
# Retrieve playlist
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


# -----------------------------------------------------------------------
# Store json as cache
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

    # print(jsonload)  # Debug
    # Stores json respones locally for faster loading.
    return file_name


# -----------------
# Transforms 3 digit number to various menu items.
# Rename this function and move back into CLI


def playSongByDigits(digits):

    # TODO: Read the cached json file instead of the API call
    response = list_playlist(pl_id)
    #   items.track.artists.name,
    #   items.track.name,
    #   items.track.id,total",
    #   additional_types=["track"],

    if digits >= 100:  # and less than 289
        print("Jukebox number: ")
        # modify 'digits' to map to a playlist index number
        # My jukebox labels start at 100 and go to 279, so we have a 0-179 song playlist
        digits = digits - 100

        # Using modified 'digits', send as index number
        track_name = response["items"][digits]["track"]["name"]
        track_id = response["items"][digits]["track"]["id"]
        print(f"Playlist Index: {digits}")
        pprint(f"Track Name: {track_name} -- Track ID: {track_id}")

        return track_id
    elif digits >= 990:  # and less than or = to 999
        print("Special number: ")
    else:
        print("ERROR: Selection not available.")


# -----------------------------------------------------------------------
# Play song from playlist
def play_song(track_selection):
    # playback_uris: list[str] = ["spotify:track:6exdwZ3EOSCjb11bd6k6Np"]

    # Transform input into list
    new_track = f"spotify:track:{track_selection}"
    playback_uris = [new_track]

    # Open Spotify App locally. Small delay so API can see it.
    # Comment out for faster testing during development
    # os.system(f"open {path}")
    # sleep(5)

    # TODO - Print NAME of device ID that you're playing on.

    print(sp_auth.start_playback(device_id, uris=playback_uris))
    # start_playback PARMS:
    # start_playback(
    #       device_id=None,
    #       context_uri=None,
    #       uris=None,
    #       offset=None,
    #       position_ms=None
    # )


# -----------------------------------------------------------------------
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


# -----------------------------------------------------------------------
# Welcome message
print(color.BOLD + "\n### Booting up Tabletop Jukebox ####" + color.END)


# -----------------------------------------------------------------------
# Dowload copy of default playlist at bootup.
response = list_playlist(pl_id)
print(f"Playlist:\n{response}")
file_prefix = "cache/playlist_" + pl_id
file_name2: str = store_local(response, file_prefix)
print(
    color.BOLD,
    color.GREEN + " # Stored Playlist locally #: " + file_name2 + color.END,
)


# -----------------------------------------------------------------------
# Take 3 digit input [100-279] and play song off playlist on default device.
# Wait for input

# Prompts user to enter number which maps to Index of playlist.
digits: int = int(input("Enter 3 digits [###]: "))
track_selection = playSongByDigits(digits)
play_song(track_selection)
print(
    color.BOLD,
    color.GREEN + "-> Playing Song -> : " + track_selection + color.END,
)
# TODO: Automate OATH2 validation

# -----------------------------------------------------------------------
# Take 3 digit input [990-999] for custom features
# -----------------------------------------------------------------------
# Take separate single button inputs to lower & raise volume
# -----------------------------------------------------------------------
# Take single button to restart song
# -----------------------------------------------------------------------
# Take single button to stop song
# -----------------------------------------------------------------------
