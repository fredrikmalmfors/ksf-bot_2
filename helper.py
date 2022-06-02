import pickle
import os
from datetime import datetime

# Get latest
def get_latest_run_folder(title, backwards_offset=0):
    history = pickle.load( open( get_history_path(title), "rb" ) )
    last_run = history[-1-backwards_offset]
    return os.path.join('data', title, last_run.isoformat('T', 'seconds'))

def create_run_folder(title):
    now = datetime.now()
    folder = os.path.join('data', title, now.isoformat('T', 'seconds'))
    os.mkdir(folder)
    return now

def get_history_path(title):
    return os.path.join('data', title, 'history.p')
