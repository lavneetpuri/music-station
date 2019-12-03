#! /usr/bin/env python3
import sys
import numpy as np
import pandas as pd
import sqlite3
from functools import reduce

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

    Usage:
    python3 db_to_csv.py subset_artist_term.db subset_artist_similarity.db subset_track_metadata.db
"""

def main(terms_file, similarity_file, metadata_file):

    terms = sqlite3.connect(terms_file)
    similarity = sqlite3.connect(similarity_file)
    metadata = sqlite3.connect(metadata_file)

    terms_cursor = terms.cursor()
    terms_cursor.execute("SELECT artist_id, group_concat(term, '|') AS terms, \
        count(artist_id) AS num_terms FROM artist_term GROUP BY artist_id")

    artist_terms = pd.DataFrame(terms_cursor.fetchall(), columns=['artist_id',
        'terms', 'num_terms'])

    terms_cursor.execute("SELECT artist_id, group_concat(mbtag, '|') AS tags, \
        count(artist_id) AS num_tags FROM artist_mbtag GROUP BY artist_id")
    artist_tags = pd.DataFrame(terms_cursor.fetchall(), columns=['artist_id',
        'tags', 'num_tags'])

    similarity_cursor = similarity.cursor()
    similarity_cursor.execute("SELECT target as artist_id, \
        group_concat(similar, '|') AS similar_artists, \
        count(target) AS num_artists FROM similarity GROUP BY target")
    artist_similarity = pd.DataFrame(similarity_cursor.fetchall(), columns=['artist_id',
        'similar_artists', 'num_artists'])

    metadata_cursor = metadata.cursor()
    metadata_cursor.execute("SELECT * FROM songs")
    song_cols = ['track_id','title','song_id','release','artist_id',
        'artist_mbid','artist_name', 'duration', 'artist_familiarity',
        'artist_hotness', 'year']
    song_metadata = pd.DataFrame(metadata_cursor.fetchall(),
        columns=song_cols)

    dfs = [artist_terms, artist_tags, artist_similarity, song_metadata]
    tracks_agg = reduce(lambda left, right: pd.merge(left,right, on='artist_id',
        how='outer'), dfs)

    tracks_agg = tracks_agg.drop(['release'], axis=1).set_index('track_id')

    tracks_agg.to_csv('from_sql.csv')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
