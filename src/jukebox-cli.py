from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pprint import pprint
import os
from time import sleep


## To do:
##  Fix oAuth flow
##  Make menus into functions.
##  Pause playback
##  Select item from playlist and play on device


path = "/Applications/Spotify.app"
device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Playlist ID
pl_id = "spotify:playlist:7D7FASC0bXRMdvfjggS0ug"
offset = 0
### https://open.spotify.com/playlist/7D7FASC0bXRMdvfjggS0ug?si=05eae12ffb2b4b6b


while True:
    print("**** Spotify Commands  ****")
    print("0 - Exit the console")
    print("1 - List Playlist")
    print("2 - List Song on Playlist")
    print("3 - Play song by ID")
    print("4 - List Devices")
    print("5 - Pause Playback")
    print("6 - Resume Playback")
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

        pprint(f"Items in Playlist: {response['items']}")

        ### print("Items in Response:")
        ### {'track': {'artists': [{'name': 'New Order'}],
        ###           'id': '1RSy7B2vfPi84N80QJ6frX',
        ###           'name': 'Blue Monday - 2016 Remaster'}}

    elif user_input == 2:
        playlist_track = int(input("Select playlist track (index) #: "))
        if playlist_track >= len(response["items"]):
            print("---> Selection is longer than list")
            print("---> Need some kind of loop here")
            break
        track_name = response["items"][playlist_track]["track"]["name"]
        track_id = response["items"][playlist_track]["track"]["id"]
        pprint(f"Track name: {track_name} -- Track id: {track_id}")

    # Play Song By ID
    elif user_input == 3:
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

        #   scope = "user-read-playback-state,user-modify-playback-state"
        #   sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

        #        device_id = "3fc94b15082d6a1206c60d9f97310d37bd5032da"
        pprint(sp.start_playback(device_id, uris=playback_uris))

        # start_playback(
        # device_id=None,
        # context_uri=None,
        # uris=None,
        # offset=None,
        # position_ms=None)

    elif user_input == 4:
        # Shows devices that can be played on
        res = sp.devices()
        pprint(res)

    elif user_input == 5:
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
        response = sp.pause_playback(device_id)
        print("Playback Paused")

    elif user_input == 6:
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
        response = sp.start_playback(device_id)
        print("Resume Playback")

    else:
        print("Please enter valid user-input.")
