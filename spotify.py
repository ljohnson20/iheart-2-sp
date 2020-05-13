import config
import datetime as dt
import spotipy
import spotipy.util as util

# Spotify API set up
username = config.spotify_username
scope = "user-library-read, playlist-modify-public"
token = config.spotify_token
secret = config.spotify_secret
uri = config.spotify_uri

playlist_id = config.spotify_playlist


def current_playlist_tracks():
    auth = util.prompt_for_user_token(username, scope, token, secret, uri)
    sp = spotipy.Spotify(auth=auth)
    playlist_cont = []
    # Getting current songs in playlist to add to list for no duplicates
    results = sp.playlist_tracks(playlist_id=playlist_id)
    while len(playlist_cont) < results['total']:
        for tracks in results['items']:
            playlist_cont.append(tracks['track']['id'])
        results = sp.playlist_tracks(playlist_id=playlist_id, offset=len(playlist_cont))
    return playlist_cont


def clear_playlist():
    auth = util.prompt_for_user_token(username, scope, token, secret, uri)
    sp = spotipy.Spotify(auth=auth)

    playlist_cont = current_playlist_tracks()
    with open(f'playlist_cont_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w') as f:
        for track_id in playlist_cont:
            f.write(f"{track_id}\n")
            sp.user_playlist_remove_all_occurrences_of_tracks(user=username, playlist_id=playlist_id, tracks=track_id)


def search_spotify(artist: str, track: str):
    auth = util.prompt_for_user_token(username, scope, token, secret, uri)
    sp = spotipy.Spotify(auth=auth)

    results = sp.search(q="artist:{} track:{} NOT Live NOT Remix".format(artist, track), type='track', limit=1)
    return results


def add_track(track_id: str):
    auth = util.prompt_for_user_token(username, scope, token, secret, uri)
    sp = spotipy.Spotify(auth=auth)

    sp.user_playlist_add_tracks(username, playlist_id, track_id)
    return True
