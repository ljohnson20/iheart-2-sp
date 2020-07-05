# Code that listens to radio station and adds songs to spotify playlist
# Has no duplicates and pushes to spotify daily? maybe hourly?
# Could also pull from website or list which might be easier

import argparse
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


# Argument parser set up
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--url', '-U', type=str, help='Set iHeart radio station url')
parser.add_argument('--info', '-I', action='store_true', help='Used to set logging to info mode')
parser.add_argument('--debug', '-D', action='store_true', help='Used to set logging to debug mode')

args = parser.parse_args()

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
if args.debug:
    logging.basicConfig(filename='listener.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
else:
    if args.info:
        logging.basicConfig(filename='listener.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    else:
        logging.basicConfig(filename='listener.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.info('Log file for station_listener.py\n\n')

# TODO - Need better try/catch blocks
try:
    if auth:
        sp = spotipy.Spotify(auth=auth)
        sp.trace = False

        # TODO - Switch url over to new reader

        url = config.iheart_url
        if args.url:
            url = args.url

        playlist_cont = spotify.current_playlist_tracks()

        if len(playlist_cont) > 250:
            spotify.clear_playlist()
            logging.info('Playlist over 250 songs! Clearing out and starting fresh')

        logging.info('Starting iHeart Radio listener')
        while True:
            auth = util.prompt_for_user_token(username, scope, token, secret, uri)
            sp = spotipy.Spotify(auth=auth)

            track_ids.clear()
            r = requests.get(url)
            if r.status_code == 200:
                artist = None
                track = None
                item = None

                try:
                    content = json.loads(r.text)
                    logging.info('iHeartRadio is listening to "' + content['title'] + '" - ' + content['artist'])
                    track = clean_string(content['title'])
                    artist = clean_string(content['artist'], False)

                    results = spotify.search_spotify(artist, track)
                    # print(results)
                    if results['tracks']['total'] == 0:
                        logging.warning(f'FAILED SPOTIFY SEARCH = artist:{artist} track:{track}')
                    else:
                        for item in results['tracks']['items']:
                            artists = []
                            for players in item['artists']:
                                artists.append(players['name'])
                            logging.info('Spotify found "' + item['name'] + '" - ' + ",".join(artists) + '\tID: ' + item['id'])
                            if item['id'] in playlist_cont:
                                x = 1
                                logging.info("Song is already in playlist")
                                logging.info('--------------------------------------------------------------')
                            else:
                                playlist_cont.append(item['id'])
                                spotify.add_track([item['id']])
                                logging.info("Song has been added to the playlist")
                                logging.info('--------------------------------------------------------------')
                except Exception as e:
                    logging.warning(f'SPOTIFY SEARCH = artist:{artist} track:{track}')
                    logging.warning(f"RESULTS = {item}")
                    logging.exception("Exception occured")
            else:
                x = 1
                logging.info('Radio station is currently playing an ad')
                logging.info('--------------------------------------------------------------')
            time.sleep(100)
    else:
        logging.error("Could not get token")
except Exception as e:
    logging.exception("Unexpected Exception occured")
