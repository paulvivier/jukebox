from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep


path = "/Applications/Spotify.app"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
print(sp)

pl_id = "spotify:playlist:5ye50Gt9kPJ14e8wdG9yiG"
offset = 0

while True:
    print("**** Spotify Commands  ****")
    print("0 - Exit the console")
    print("1 - List Playlist")
    print("2 - Play song from Playlist")
    print("3 - List Devices")
    user_input = int(input("Enter Your Choice: "))

    # Default - Exit
    if user_input == 0:
        print("Good Bye. Have a great day!")
        break

    # List Playlist
    elif user_input == 1:
        response = sp.playlist_items(
            pl_id,
            offset=offset,
            fields="items.track.artists.name,items.track.name,items.track.id,total",
            additional_types=["track"],
        )

        if len(response["items"]) == 0:
            break

        pprint(response["items"])
        offset = offset + len(response["items"])
        print(offset, "/", response["total"])
        offset = 0

    # Play Song from Playlist
    elif user_input == 2:
        # track_selection = str(input("Enter Track ID: "))
        # Shows playing devices
        os.system(f"open {path}")
        sleep(5)
        res = sp.devices()
        pprint(res)

        scope = "user-read-playback-state,user-modify-playback-state"
        sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
        # playback_uris='uris=["spotify:track:6exdwZ3EOSCjb11bd6k6Np"]'

        # Forces device to playback on, even if it's timed out ('is_active': False)
        transfer_playback = sp.transfer_playback(
            "3fc94b15082d6a1206c60d9f97310d37bd5032da"
        )
        playsong = sp.start_playback(uris=["spotify:track:6exdwZ3EOSCjb11bd6k6Np"])

        # Change volume
        # sp.volume(100)
        # sleep(2)
        # sp.volume(50)
        # sleep(2)
        # sp.volume(100)

    elif user_input == 3:
        res = sp.devices()
        pprint(res)

    # start_playback(
    # device_id=None,
    # context_uri=None,
    # uris=None,
    # offset=None,
    # position_ms=None)

    else:
        print("Please enter valid user-input.")
