import os
import googleapiclient.discovery
import googleapiclient.errors
import pickle
from datetime import datetime
from helper import get_history_path, get_latest_run_folder, create_run_folder
from credentials import YOUTUBE_API_KEY

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def setup_proxy():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YOUTUBE_API_KEY)
    return youtube


def get_videos(youtube, playlist_id):
    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos


def main(project):

    title = project['title']

    print('Fetching', title)

    if not os.path.isdir('data/' + title):
        print('.... for the first time!')
        os.mkdir('data/' + title)

    youtube = setup_proxy()
    videos = get_videos(youtube, project['youtube_playlist_id'])

    try:
        history = pickle.load(open(get_history_path(title), "rb"))
        last_run = history[-1]
        videos = list(filter(lambda x: datetime.fromisoformat(
            x['snippet']['publishedAt'][:-1]) > last_run, videos))
    except:
        history = []
        pickle.dump(history, open(get_history_path(title), "wb"))

    # Create new data folder
    if len(videos):
        print(len(videos), 'new videos!')
        now = create_run_folder(title)
        history.append(now)
        pickle.dump(history, open(get_history_path(title), "wb"))
        pickle.dump(videos, open(os.path.join(
            get_latest_run_folder(title), 'videos.p'), 'wb'))
        return True

    else:
        print('No new videos.')
        return False
