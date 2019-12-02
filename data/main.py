import pandas as pd
import os

dir_path = os.path.dirname(__file__)

songs = pd.read_csv(os.path.join(dir_path, 'songs.csv'), index_col='track_id')

# TODO: filter invalid rows
# we are losing too much data
# songs = songs[songs.year != 0]

artists = pd.read_csv(
            os.path.join(dir_path, 'artists.csv'), index_col='artist_id'
          )
# drop row count column
artists = artists.drop(artists.columns[0], 1)
