import config
import datetime as dt
import spotipy
import spotipy.util as util
import os

# Spotify API set up
username = config.spotify_username
scope = "user-library-read, playlist-modify-public"
client = config.spotify_client
secret = config.spotify_secret
uri = config.spotify_uri

# TODO - Swap config id to variable in functions to avoid mix up
# TODO - Fix Spotify token generation. Maybe also pass through function?
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
