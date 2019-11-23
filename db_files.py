#! /usr/bin/env python3
import sys
import numpy as np
import pandas as pd
"""
    The columns (16) contained the in DataFrame are:
    track_id, song_id, title, artist_name, duration, year, artist_mbid, 
    artist_id, artist_tags, num_tags, artist_terms, num_terms, similar_artists, 
    num_artists, artist_hotness, artist_familiarity 
    The features(s) that are excluded are:
    release (album)
    The data was spread across three different databases. The tables of each database
    were combined into one. From there a query was created to JOIN the different tables together.
    
    NOTE: There are some songs that have NULL/irrelevant columns 
    (ex. artist tags (6290), artist terms (5), year of 0 (5320))
    (Using INNER JOIN (3703))
"""

def read_data(filename):
    return pd.read_csv(filename)

def main(filename):

    # Read in the tracks_agg.csv (7MB) file 

    songs = read_data(filename)

    # TODO: 
    # - Similar artist column contains a string of artist ids separated by "|"
    # -- Should we display artist names instead?

if __name__ == '__main__':
    main(sys.argv[1])
