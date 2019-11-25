import pandas as pd
import numpy as np
import h5py
import os, sys

################################################################
# Script used for aggregating 10000 songs dataset obtained from
# http://millionsongdataset.com/pages/getting-dataset/#subset
# into a single csv tar.gz file. Because raw data is structured using
# Hierarchical Data Format, the output of this script will
# simplify access to data for further analysis.
#
# - Usage - - -
# python3 main.py <raw_dataset_dir> <output_file>
# Pass path to the dataset folder and output file name
# as first and second command line arguments, respectively.
# e.g. python3 h5_to_csv.py ../MillionSongSubset output.csv
#
# - Note - - -
# Be mindful of the size of the raw dataset:
# Collapsing big HDF into large files may not be compatible
# with your file system. Increase num_out_files if you notice issues.
################################################################

# the fields we want to extract from the raw dataset.
# these will form the header of the csv output
output_schema = [
    'track_id',
    'title',
    'artist_id',
    'tempo',
    'song_hotttnesss',
    # 7 song mode: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian and Locrian
    'mode',
    'mode_confidence',
    # e.g. F minor
    'key',
    'key_confidence',
    'loudness',
    'energy',
    'duration',
    # how suitable a track is for dancing
    'danceability',
    # song can be associated with many tracks (with very slight audio differences
    # 'songid'
    # likely unrealistic for analysis
    'end_of_fade_in',
    'start_of_fade_out',
    'analysis_sample_rate'
]

# returns a pandas dataframe containing single valued song info.
# 1 dimensional info such as beats/segments is omitted for now.
def parse_song(filename):
    song = h5py.File(filename, 'r')
    
    song_info = pd.DataFrame(song['metadata']['songs'][:])
    # combine info from analysis
    song_info = song_info.join(pd.DataFrame(song['analysis']['songs'][:]))
    return song_info

def main(dataset_path, output_file):
    songs = pd.DataFrame(columns=output_schema)
    for root, dirs, files in os.walk(os.path.join(dataset_path, 'data')):
        for filename in files:
            # skip non h5 files
            if not filename.endswith('.h5'):
                continue

            song = parse_song(os.path.join(root, filename))

            # keep only fields specified in the schema and merge with songs
            song = song[output_schema]
            songs = pd.concat([songs, song])

    # write as csv file
    # TODO: remove b string prefix from dataframe
    songs = songs.set_index('track_id')
    songs.to_csv(output_file)

if __name__ == '__main__':
    dataset_path = sys.argv[1]
    output_file = sys.argv[2]
    main(dataset_path, output_file)