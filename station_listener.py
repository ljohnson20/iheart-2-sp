# Code that listens to radio station and adds songs to spotify playlist
# Has no duplicates and pushes to spotify daily? maybe hourly?
# Could also pull from website or list which might be easier

import config
import re
import logging
import time
import requests
import spotify
import spotipy
import spotipy.util as util
import json


# Used for doctering up the track and artist name for searching
def clean_string(string: str, remove_extra: bool = True):
    removal = ['feat', 'featuring']
    if remove_extra:
        temp = re.sub('[  ]+', ' ', re.sub('[^A-Za-z0-9$ñ& -]+', '', string.lower()))
    else:
        temp = re.sub('[  ]+', ' ', re.sub('[^A-Za-z0-9$ñ -]+', '', string.lower()))
    temp = temp.split()
    fixed = [word for word in temp if word not in removal]
    doctored = ' '.join(fixed)
    return doctored


# Used to get api url from base iHeart Radio station url
def api_url_find(iheart_url: str):
    main = requests.get(iheart_url)
    split = main.text[main.text.find("@id"):main.text.find("@type", main.text.find("@id"))].split('"')[2].split("/")
    if len(split) != 0:
        live = split[2].split("/")
        if len(live) != 0:
            api_url = "https://us.api.iheart.com/api/v3/live-meta/stream/" + live[-1] + "/currentTrackMeta"
            return api_url
    return None


# Spotify API set up
username = config.spotify_username
scope = "user-library-read, playlist-modify-public"
token = config.spotify_token
secret = config.spotify_secret
uri = config.spotify_uri

auth = util.prompt_for_user_token(username, scope, token, secret, uri)

playlist_id = config.spotify_playlist
track_ids = []
playlist_cont = []

# https://developer.spotify.com/documentation/web-api/reference/

# Logs set up
logging.basicConfig(filename='listener.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.info('Log file for station_listener.py\n\n')

try:
    if auth:
        sp = spotipy.Spotify(auth=auth)
        sp.trace = False

        url = config.iheart_url

        playlist_cont = spotify.current_playlist_tracks()

        while True:
            auth = util.prompt_for_user_token(username, scope, token, secret, uri)
            sp = spotipy.Spotify(auth=auth)

            track_ids.clear()
            r = requests.get(url)
            if r.status_code == 200:
                content = json.loads(r.text)
                print('iHeartRadio is listening to "' + content['artist'] + '" - ' + content['title'])
                track = clean_string(content['title'])
                artist = clean_string(content['artist'], False)

                results = spotify.search_spotify(artist, track)
                # print(results)
                if results['tracks']['total'] == 0:
                    logging.warning(f'FAILED SPOTIFY SEARCH = artist:{artist} track:{track}')
                    print("No results were found on Spotify")
                else:
                    for item in results['tracks']['items']:
                        artists = []
                        for players in item['artists']:
                            artists.append(players['name'])
                        print('Spotify found "' + item['name'] + '" - ' + ",".join(artists) + '\tID: ' + item['id'])
                        if item['id'] in playlist_cont:
                            x = 1
                            print("Song is already in playlist")
                            print('--------------------------------------------------------------')
                        else:
                            playlist_cont.append(item['id'])
                            track_ids.append(results['tracks']['items'][0]['id'])
                            # sp.user_playlist_add_tracks(username, playlist_id, track_ids)
                            print("Song has been added to the playlist")
            else:
                x = 1
                print('Radio station is currently playing an ad')
                print('--------------------------------------------------------------')
            time.sleep(100)
    else:
        logging.error("Could not get token")
except Exception as e:
    logging.debug(f'SPOTIFY SEARCH = artist:{artist} track:{track}')
    logging.debug(f"RESULTS = {item['id']}")
    logging.exception("Exception occured")
