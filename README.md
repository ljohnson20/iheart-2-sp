[![Build Status](https://drone.lokyra.org/api/badges/ljohnson20/iheart-2-sp/status.svg?ref=refs/heads/master)](https://drone.lokyra.org/ljohnson20/iheart-2-sp)

Script that monitors a iHeart radio station and automatically adds the song to Spotify playlist.

Requires the config file to be filled out with spotify api which can be created [here](https://developer.spotify.com/dashboard/login). For the playlist id go to spotify web player or app, right click on a playlist that you created, and select copy playlist link/uri. It should look something like this "spotify:playlist:37i9dQZEVXbLRQDuF5jeBp".

The iHeart url should just be the base station url. Example: ["https://www.iheart.com/live/z100-1469/"]()

Then just run the station_listener script to start gathering songs