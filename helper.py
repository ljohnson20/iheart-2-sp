import config
import datetime as dt
import re
import requests
import spotipy
import os

# TODO - Maybe pass variables all from station_listener don't set them up here?
# Variable set up
scope = "user-library-read, playlist-modify-public"
if "spotify_username" and "spotify_client" and "spotify_secret" and "spotify_uri" in os.environ:
    username = os.environ.get(spotify_username)
    client = os.environ.get(spotify_client)
    secret = os.environ.get(spotify_secret)
    uri = os.environ.get(spotify_uri)
else:
    username = config.spotify_username
    client = config.spotify_client
    secret = config.spotify_secret
    uri = config.spotify_uri

if "spotify_playlist" in os.environ:
    playlist_id = os.environ.get(spotify_playlist)
else:
    playlist_id = config.spotify_playlist


def current_playlist_tracks():
    token = spotipy.util.prompt_for_user_token(username, scope, client, secret, uri)
    sp = spotipy.Spotify(auth=token)
    playlist_cont = []
    # Getting current songs in playlist to add to list for no duplicates
    results = sp.playlist_tracks(playlist_id=playlist_id)
    while len(playlist_cont) < results['total']:
        for tracks in results['items']:
            playlist_cont.append(tracks['track']['id'])
        results = sp.playlist_tracks(playlist_id=playlist_id, offset=len(playlist_cont))
    return playlist_cont


def clear_playlist():
    token = spotipy.util.prompt_for_user_token(username, scope, client, secret, uri)
    sp = spotipy.Spotify(auth=token)

    playlist_cont = current_playlist_tracks()
    with open(f'playlist_cont_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w') as f:
        for track_id in playlist_cont:
            f.write(f"{track_id}\n")
            sp.user_playlist_remove_all_occurrences_of_tracks(user=username, playlist_id=playlist_id, tracks=[track_id])

    return 0


def read_playlist_file(file: str):
    if os.path.isfile(file) and os.path.exists(file):
        with open(file, 'r') as f:
            for track_id in f.readlines():
                add_track([track_id])

        return 0
    else:
        return 1


# TODO - May need to account for songs with remix in name
def search_spotify(artist: str, track: str):
    token = spotipy.util.prompt_for_user_token(username, scope, client, secret, uri)
    sp = spotipy.Spotify(auth=token)

    track_id = None
    artists = None
    name = None
    popularity = None

    results = sp.search(q=f"artist:{artist} track:{track} NOT Live NOT Remix", type='track', limit=1)
    if results['tracks']['total'] != 0:
        track_id = results['tracks']['items'][0]['id']
        artists = results['tracks']['items'][0]['artists']
        name = results['tracks']['items'][0]['name']
        popularity = results['tracks']['items'][0]['popularity']
    return track_id, artists, name, popularity


def add_track(track_id: list):
    token = spotipy.util.prompt_for_user_token(username, scope, client, secret, uri)
    sp = spotipy.Spotify(auth=token)

    sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_id)
    return 0

# TODO - Need to remove duplicates using fuzzy string match
# TODO - Remove unpopular songs


# Used for doctering up the track and artist name for searching
def clean_string(string: str, remove_extra: bool = True):
    removal = ['the', 'feat', 'feat.', 'featuring']
    if remove_extra:
        temp = re.sub('[  ]+', ' ', re.sub(r"[^A-Za-z0-9$ñ&\. -]+", '', string.lower()))
    else:
        temp = re.sub('[  ]+', ' ', re.sub(r"[^A-Za-z0-9ñ&$\. -]+", '', string.lower()))
    temp = temp.split()
    fixed = [word for word in temp if word not in removal]
    doctored = ' '.join(fixed)
    return doctored


# Used to get api url from base iHeart Radio station url
def api_url_find(iheart_url: str):
    main = requests.get(iheart_url)
    if main.status_code == 200:
        split = main.text[main.text.find("@id"):main.text.find("@type", main.text.find("@id"))].split('"')[2].split("/")
        if len(split) != 0:
            live = split[2].split("/")
            if len(live) != 0:
                api_url = "https://us.api.iheart.com/api/v3/live-meta/stream/" + live[-1] + "/currentTrackMeta"
                return api_url
    return None