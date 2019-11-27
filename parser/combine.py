#! /usr/bin/env python3
import sys
import numpy as np
import pandas as pd


"""
Data source:
http://millionsongdataset.com/pages/getting-dataset/#subset

Script used to combined the metadata from the various database files and 
directory of h5 files into a single csv file.

Script used to combined the aggregated metadata and analysis from the database
and h5 files into a single csv file. 

Usage:
python3 combine.py from_sql.csv from_h5.csv

"""


def main(file1, file2):

    # Read the files in!
    metadata = pd.read_csv(file1)
    analysis = pd.read_csv(file2)

    # Join the metadata and the analysis data together
    join_keys = ['track_id', 'duration', 'artist_id', 'title']
    combined = metadata.merge(analysis, on=join_keys, how='inner')

    # The 17 columns that contain the relevant data to analyze
    desired_columns = [
        'track_id', 'title', 'artist_id', 'year', 'tempo', 'song_hotttnesss',
        'mode','mode_confidence','key', 'key_confidence', 'loudness', 'energy',
        'duration','danceability', 'end_of_fade_in', 'start_of_fade_out',
        'analysis_sample_rate'
    ]

    # Filter the desired columns
    combined = combined[desired_columns].set_index('track_id')

    # Write the file to a csv
    combined.to_csv('songs.csv')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
