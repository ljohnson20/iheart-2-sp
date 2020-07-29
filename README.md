[![Build Status](https://drone.lokyra.org/api/badges/ljohnson20/iheart-2-sp/status.svg?ref=refs/heads/master)](https://drone.lokyra.org/ljohnson20/iheart-2-sp) 
[![CodeCov](https://codecov.io/gh/ljohnson20/iheart-2-sp/branch/master/graph/badge.svg)](https://codecov.io/gh/ljohnson20/iheart-2-sp)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Script that monitors a iHeart radio station and automatically adds the song to Spotify playlist.

Requires the config file to be filled out with spotify api which can be created 
[here](https://developer.spotify.com/dashboard/login). For the playlist id go to spotify web player or app, 
right click on a playlist that you created, and select copy playlist link/uri. It should look something like 
this "spotify:playlist:37i9dQZEVXbLRQDuF5jeBp".

The iHeart url should just be the base station url. Example: ["https://www.iheart.com/live/z100-1469/"]()

Then just run the station_listener script to start gathering songs. Can be run with the following command line arguments.

```
--url = Set iHeart radio station url. Defaults to config file

--info = Used to set logging to info mode

--debug = Used to set logging to debug mode

--limit = Set upper limit of playlist size. Defaults to 250 songs then clears out id list to text file

--help = Display help for station_listener.py
```

Still a work in progress and more of a learning tool than anything.
