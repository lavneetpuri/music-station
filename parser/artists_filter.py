#! /usr/bin/env python3
import sys
import numpy as np
import pandas as pd


"""
Data source:
http://millionsongdataset.com/pages/getting-dataset/#subset

Script used to filter the important information about all artists (3888)

'artist_id', 'artist_name'

Contains artist ids that are similar to the artists
'similar_artists', 'num_artists'

Contains tags that are similar to genre
'artist_tags', 'num_tags'

Similar to tags but have a much larger variety of terms
'artist_terms', 'num_terms'

Indication of how popular the artists was in 2010
'artist_hotness'

Indication of how well known the artist was in 2010
'artist_familiarity'

Usage:
python3 artist_filter.py from_sql.csv

"""


def main(file1):

    # Read the files in!
    artists = pd.read_csv(file1)

    # The 10 columns that contain the relevant data to analyze
    desired_columns = [
        'artist_id', 'artist_name', 'similar_artists', 'num_artists',
        'artist_tags', 'num_tags', 'artist_terms', 'num_terms',
        'artist_hotness', 'artist_familiarity'
    ]

    # Filter the desired columns
    artists = artists[desired_columns]

    # Drop the duplicate rows with the same artist id
    artists = artists.drop_duplicates(subset='artist_id', keep='first')

    # Write the file to a csv
    artists.to_csv('artists.csv')


if __name__ == '__main__':
    main(sys.argv[1])
