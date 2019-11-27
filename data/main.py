import pandas as pd
import os

dir_path = os.path.dirname(__file__)
songs = pd.read_csv(os.path.join(dir_path, 'songs.csv'))
