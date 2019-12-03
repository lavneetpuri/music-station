import numpy as np
import sys
from .song import Song
from data.main import songs

# returns random list of track ids of length between 5 t 10
def rand_tracks():
    rand_num = np.random.randint(5,10)
    rand_sample = songs.sample(rand_num)
    return rand_sample.index.values

# keeps track of name and song list
class PlayList:
    def __init__(self, name, track_list=None):
        self.name = name
        track_list = track_list or rand_tracks()
        try:
            self.songs = list(map(lambda id: Song(id),track_list))
        except ValueError as v:
            print(v)
            print('songs not initialized')
