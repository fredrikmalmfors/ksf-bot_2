import pickle
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from helper import get_latest_run_folder

scope = "playlist-modify-public, playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def main(proj):

    print('')
    title = proj['title']
    sids = pickle.load(
        open(os.path.join(get_latest_run_folder(title), "sids.p"), "rb"))

    while len(sids):

        sp.playlist_add_items(
            proj['spotify_playlist_id'],
            sids[:100]
        )

        print('Successfully added', len(sids[:100]), 'songs to playlist.')

        sids = sids[100:]

    print('DONE')
    return True
