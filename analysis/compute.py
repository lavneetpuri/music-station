import pandas as pd
from data.main import songs
from model.playlist import PlayList

"""
Given a songs dataframe subset (user's preferred song list),
return user's and recommended Playlist instances
as a tuple
Params:
songs_subset - subset of `songs` chosen by the user
rec_size - length of recommended playlist
"""
def get_playlists(songs_subset, rec_size=8):
    assert isinstance(songs_subset, pd.DataFrame)

    # Get the median features of the input playlist
    X0 = songs_subset.median()

    # filter input playlist from `songs`
    X = songs.drop(songs_subset.index)
    # filter X to numeric columns with non-null rows only
    # TODO: should fade_in and fade_out be included finding closest?
    X = songs.drop(['end_of_fade_in', 'start_of_fade_out'], 1) \
             .select_dtypes(['number']) \
             .dropna()

    # series with relative distance to median of `songs_subset` (X0)
    # of every track in `songs` minus `songs_subset`
    distances = (X-X0).pow(2).sum(1).pow(0.5)

    # return `rec_size` song ids with closest distance to median
    rec_songs = distances.sort_values().head(rec_size).index.values
    input_songs = songs_subset.index.values

    user_playlist = PlayList('Your Playlist', list(input_songs))
    rec_playlist = PlayList('Recommended Playlist', list(rec_songs))

    return user_playlist, rec_playlist


    