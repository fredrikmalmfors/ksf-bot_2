import youtube
import parse
import sp_search
import manual
import sp_add
import pickle
import os
from helper import get_latest_run_folder

# Don't do it for now
do_repair = False

projects = [
    {
        'title': 'ksf',
        'youtube_playlist_id': 'UUud3lmIRcld41IocSMIT71w',
        'spotify_playlist_id': '0sqb6S2S8pray0Sc8GCre0'
    }, {
        'title': 'ksf_100t',
        'youtube_playlist_id': 'UU5VCniQNgJTbxtiXXHKRs0w',
        'spotify_playlist_id': '2RtzChRj6A9COe6LaL47p7'
    }, {
        'title': 'krealington',
        'youtube_playlist_id': 'UUNMLvFabOIRIMx-H7Vv9law',
        'spotify_playlist_id': '29chcJ9iPvVAXX4r5Rnny4'
    }, {
        'title': 'warble',
        'youtube_playlist_id': 'UUGvgxDMpKyliTpy83S-VTLw',
        'spotify_playlist_id': '44XFW9vxaOQr6cC3Vxw9as'
    },
    # {
    #     'title': 'nightmare_surf',
    #     'youtube_playlist_id': 'UUQWddkZJilpA3iqi4dO7M9w',
    #     'spotify_playlist_id': 'jibberish'
    # }
]

for proj in projects:

    print(' ')
    print(f"<-------------- {proj['title']} -------------->")
    print(' ')

    success = True

    # First, check repair
    if do_repair:
        try: 
            chocies = pickle.load( open( os.path.join(get_latest_run_folder(proj['title']), "choices.p"), "rb" ) )
            ksfs_done = pickle.load( open( os.path.join(get_latest_run_folder(proj['title']), "ksfs_done.p"), "rb" ) )
        except:
            chocies = []
            ksfs_done = []

        if len(ksfs_done) == len(chocies):

            success = youtube.main(proj)

            if success:
                success = parse.main(proj)

            if success:
                success = sp_search.main(proj)

        else:
            print('MISMATCH! NOT DONE YET I GUESS!')
            print(os.path.join(get_latest_run_folder(proj['title'])))
            print(len(ksfs_done), 'vs', len(chocies))
    else:
        success = youtube.main(proj)

        if success:
            success = parse.main(proj)

        if success:
            success = sp_search.main(proj)

    if success:
        success = manual.main(proj)

    if success:
        success = sp_add.main(proj)
        
    if success:
        print('SUCCESS')


