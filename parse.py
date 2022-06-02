import pickle
import re
import pprint
import os

from helper import get_latest_run_folder

err_count = 0

def blank():
    global err_count
    print('\n\n\n')
    err_count += 1


def get_description(video):
    return video['snippet']['description'].splitlines()


def cleanup_song_string(line, index=0):

    # Init starting index
    rest = line[index:]
    stack = [line, rest]

    # Dismiss if url
    reg = re.search("youtube.com", rest)
    if reg:
        return

    reg = re.search("picked by", rest)
    if reg:
        return

    reg = re.search("suggested by", rest)
    if reg:
        return

    # Remove junk start
    while True:
        try:
            if rest and (not rest[0].isalnum()):
                rest = rest[1:]
                stack.append(rest)
            else:
                break
        except:
            blank()
            print('Parse error. Stack:')
            print(pprint.pprint(stack))
            break

    # Remove first hyphen
    if rest:
        to_replace = [' - ',' -- ',' – ']
        for el in to_replace:
            if rest.count(el):
                rest = rest.replace(el, ' ', 1)

        return rest

    
def get_songs(description):
    songs = []
    active = 0
    for line in description:

        if active:
            if line:
                if '-----------' in line:
                    active = 0
                else:
                    song = cleanup_song_string(line)
                    songs.append(song)
            else:
                if active == 2:
                    active = 1
                elif active == 1:
                    active = 0

        # Yes, very good regex
        reg = re.search("^(song|Song|SONG|Music|music|MUSIC|SOUNDTRACK|Soundtrack|soundtrack)", line)
        if reg:
            index = reg.span()[1]
            song = cleanup_song_string(line, index)
            songs.append(song)
            if active == 0:
                active = 2

    songs = [song for song in songs if (song and (len(song.strip()) > 2))]
    
    print('---------- Description ---------')
    pprint.pprint(description)
    print('----------- END -----------')
    if len(songs) == 0:
        print('No songs found in this video :(')
    else:
        print('Songs found:')
        for song in songs:
            print(f'--> {song}')

    blank()

    return songs

def main(proj):

    title = proj['title']

    videos = pickle.load( open( os.path.join(get_latest_run_folder(title), "videos.p"), "rb" ) )

    descriptions = list(map(get_description, videos))

    all_songs = list(map(get_songs, descriptions))

    # Flatten
    all_songs_flat = [item for sublist in all_songs for item in sublist]

    print(' ')
    print('RESULT: ')
    print(' ')
    print('Videos:                  ', len(videos))
    print(' ')
    print('Videos without songs:    ', err_count)
    print(' ')
    print('Songs in total:          ', len(all_songs_flat))

    pickle.dump(all_songs_flat, open(os.path.join(get_latest_run_folder(title), 'songs.p'), 'wb'))

    return True


