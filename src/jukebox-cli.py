from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep


##  TODO
##  Fix oAuth flow (DONE!)
##  Make menus into functions. (DONE!)
##  Start play on device from playlist index selection
##  Map Numbers 100 - 279 to playlist index


path = "/Applications/Spotify.app"

# You'll need these ENVs in your shell. https://developer.spotify.com/
# SPOTIPY_CLIENT_ID=
# SPOTIPY_CLIENT_SECRET=
# SPOTIPY_REDIRECT_URI=


# Device options until you can add ability to specify a different one.
device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"  # laptop
# device_id = "78776d6cc7f769f4ea5e302aa41977e9211af158"  # phone

scope = (
    "user-read-playback-state,user-modify-playback-state,app-remote-control,streaming"
)

# Authentication options. _May_ need to create a flow for reauthenticating.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
sp_auth = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Playlist ID
pl_id = "spotify:playlist:7D7FASC0bXRMdvfjggS0ug"
offset = 0
### https://open.spotify.com/playlist/7D7FASC0bXRMdvfjggS0ug?si=05eae12ffb2b4b6b


# Retrives usable fields from the playlist.
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
# UPDATE - Maybe the playist scope isn't needed though
def song_details(pl_id):
    response = list_playlist(pl_id)
    # response = sp.playlist_items(
    #     pl_id,
    #     offset=offset,
    #     fields="items.track.artists.name,items.track.name,items.track.id,total",
    #     additional_types=["track"],
    # )

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
    print(color.BOLD + "0" + color.END + " - Exit the console")
    print(color.BOLD + "1" + color.END + " - List Playlist")
    print(color.BOLD + "2" + color.END + " - List Song on Playlist")
    print(color.BOLD + "3" + color.END + " - Play song by ID")
    print(color.BOLD + "4" + color.END + " - List Devices")
    print(color.BOLD + "5" + color.END + " - Pause Playback")
    print(color.BOLD + "6" + color.END + " - Resume Playback")
    user_input = int(input(color.BOLD + "Enter Your Choice: " + color.END))

    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")
        break

    # List Playlist
    elif user_input == 1:
        ## ISSUE with Typing . Likely force this into a type, but which?
        response = list_playlist(pl_id)
        pprint(f"Items in Playlist: {response['items']}")

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
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
        response = sp.pause_playback(device_id)
        print(color.BOLD, color.RED + " * Playback Paused * " + color.END)

    elif user_input == 6:
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
        response = sp.start_playback(device_id)
        print(color.BOLD, color.GREEN + " > Playback Resumed > " + color.END)

    else:
        print("Please enter valid user-input.")
