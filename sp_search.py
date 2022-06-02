import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle
import os
              
scope = "user-library-read"

from helper import get_latest_run_folder

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope),
    retries=10,
    status_retries=10,
    status_forcelist=(404,),
    backoff_factor=1
)

all_markets = ['SE', 'US', 'CA', 'AU', 'GB']

def res_to_list(item):
    return {
        'id': item['id'],
        'show': " & ".join([artist['name'] for artist in item['artists']]) 
            + ' ~ ' + item['name']
    }

def main(proj):

    title = proj['title']
    songs = pickle.load( open( os.path.join(get_latest_run_folder(title), "songs.p"), "rb" ) )
    exp = []
    count = 0

    for song in songs:
        if not song:
            continue

        count += 1
        if count % 10 == 0:
            print(count)

        print('Searching for:', song)

        res = sp.search_markets(
            song,
            limit=20,
            markets=all_markets
        )

        # Merge
        items = []
        for market in all_markets:
            items.extend(res[market]['tracks']['items'])

        if len(items) == 0:
            continue

        # remove duplicates
        seen = set()
        ritems = []

        for item in items:
            if not item['id'] in seen:
                ritems.append(item)
            seen.add(item['id'])
            
        choices = list(map(res_to_list, 
            ritems
        ))

        # This shouldn't be named ksf 
        # but I don't want to ruin the previous data compatibility at this stage
        fin = {
            'ksf': song,
            'res': choices
        }

        exp.append(fin)

    pickle.dump(exp, open(os.path.join(get_latest_run_folder(title), 'choices.p'), 'wb'))
    return True
