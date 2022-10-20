from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep


path = "/Applications/Spotify.app"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
print(sp)

# Playlist ID
pl_id = "spotify:playlist:5ye50Gt9kPJ14e8wdG9yiG"
offset = 0

while True:
    print("**** Spotify Commands  ****")
    print("0 - Exit the console")
    print("1 - List Playlist")
    print("2 - Play song by ID")
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

        ### print("Items in Response:")
        ### {'track': {'artists': [{'name': 'New Order'}],
        ###           'id': '1RSy7B2vfPi84N80QJ6frX',
        ###           'name': 'Blue Monday - 2016 Remaster'}}

        # pprint(response["items"][0]["track"]["name"])
        # pprint(response["items"][0]["track"]["id"])

        playlist_track = int(input("Select playlist track #: "))
        if playlist_track >= len(response["items"]):
            print("---> Selection is longer than list")
            print("---> Need some kind of loop here")
            break
        track_name = response["items"][playlist_track]["track"]["name"]
        track_id = response["items"][playlist_track]["track"]["id"]
        pprint(f"Track name: {track_name} -- Track id: {track_id}")

    # Play Song By ID
    elif user_input == 2:
        playback_uris: list[str] = ["spotify:track:6exdwZ3EOSCjb11bd6k6Np"]
        track_selection = str(input("Enter Track ID: "))
        new_track = f"spotify:track:{track_selection}"
        playback_uris = [new_track]

        # Open Spotify App locally. Small delay so API can see it.
        # Comment out for faster testing during development
        # os.system(f"open {path}")
        # sleep(5)

        # Shows playing devices
        res = sp.devices()
        pprint(res)

        scope = "user-read-playback-state,user-modify-playback-state"
        sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

        device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"
        pprint(sp.start_playback(device_id, uris=playback_uris))

        # Change volume
        # sp.volume(100)
        # sleep(2)
        # sp.volume(50)
        # sleep(2)
        # sp.volume(100)

    elif user_input == 3:
        # Shows devices that can be played on
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
