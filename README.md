# jukebox
 
I bought a tabletop jukebox at an antique store and had the idea that it would be nice to be able to use it and make it play. Play what? Spotify. They have some pretty amazing APIs, so the journey shouldn't be too painful. 

## Overview

The tabletop jukebox that I have has a mechanical 12 button keypad, which means that at some point each button is simply closing a circuit. Connect those switches to a low voltage that can be measured by the inputs of a Raspberry PI. Read those inputs in Python. Run a python program on the Raspberry Pi to do the rest of the work too. Send the  number pad to a mapping list which translates them to the spotify playlist order. Select the song on the playlist. Tell spotify to play the selected song on the desired device. And then we're dancing! 

## How to use it
Developed on Python 3.10 


### Install dependancies:
- Spotipy (note the 'py' instead of 'fy')
    - `pip install spotipy`

### Set ENV variables
- Create an account on [Spotify's Developer site](https://developer.spotify.com/) . 
- Link your premium spotify account to it.
- Set up an "application" which will give you values for these three variables.
    - `SPOTIPY_CLIENT_ID`
    - `SPOTIPY_CLIENT_SECRET`
    - `SPOTIPY_REDIRECT_URI`



![Jukebox Image](images/tabletop_jukebox.jpg)
