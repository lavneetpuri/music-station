from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from data.main import songs
import pandas as pd
import numpy as np

NUM_CLUSTERS = 10

# dimensions for principle component analysis
NUM_DIMENSIONS = 2

# return songs with only relevant info for clustering
def filter_songs(remove_cols):
    # column not needed for clustering
    return songs.drop(remove_cols, 1) \
                .dropna()

# find `n` clusters in given dataframe `X`
# returns array with integer labels
# for row i in `X` corresponding to index i
def get_clusters(X, n):
    model = make_pipeline(
        KMeans(n_clusters=n)
    )
    model.fit(X)
    return model.predict(X)

# reduce `X` dataframe to only `n` dimensions with most interesting features
# returns array with shape (m,n)
def get_pca(X, n):
    flatten_model = make_pipeline(
        MinMaxScaler(),
        PCA(n),
    )
    return flatten_model.fit_transform(X)

# returns original songs df with cluster labels
# new df may be smaller due to filtering of invalid rows
def get_labeled_songs(X, clusters, add_cols):
    labeled_songs = X.copy()
    labeled_songs['label'] = clusters
    for col_name in add_cols:
        labeled_songs[col_name] = songs[col_name]
    return labeled_songs


# https://stackoverflow.com/questions/46908388/find-euclidean-distance-from-a-point-to-rows-in-pandas-dataframe?rq=1
def get_distances(origin, pts):
    distance = (pts[['X', 'Y']] - np.array(origin)).pow(2).sum(1).pow(0.5)
    return distance

"""
Pre:
Param:
    cluster_data: contains information about row, 2D coordinates from PCA,
    and the cluster labeled given from KMeans
Post:
    Returns the rows of the 5 closest points to a given input point
"""
def get_closest_pts(cluster_data):

    # Assume that the last point is our input point
    target_pt = cluster_data.tail(1)

    # Coordinates of the input point
    coords = target_pt[['X','Y']]

    # Cluster value of the input point
    target_cluster = target_pt['cluster'].values[0]

    # Get all the points of the cluster that the input point belongs to
    # Need to .copy(deep=True) to remove warning
    cluster_points = cluster_data[cluster_data['cluster'] == target_cluster].copy(deep=True)

    # Now take the distance between input point and the points in the cluster
    cluster_points['distance'] = get_distances(coords, cluster_points)

    # Return the 5 closest points to the input point
    # We do the .head(6) because the input point is in the cluster dataset still
    # Then take the range from the second point and on
    cluster_points = cluster_points.sort_values(['distance']).head(6)[1:]
    return cluster_points

# Get 5 random songs
playlist = songs.sample(5)

# Get the median features of the playlist
list_med = playlist.median()

# Append the median features of the playlist into the songs dataset
songs.loc['PLAYLIST_MEDIAN'] = list_med

irrelevant_cols = ['title', 'artist_id']
# TODO: should these be included?
irrelevant_cols.extend(['end_of_fade_in', 'start_of_fade_out'])

X = filter_songs(irrelevant_cols)
clusters = get_clusters(X, NUM_CLUSTERS)

labeled_songs = get_labeled_songs(X, clusters, add_cols=irrelevant_cols)

songs_principle = get_pca(X, NUM_DIMENSIONS)

# Get the coordinates and labels of the dataset from PCA and clustering
cluster = pd.DataFrame({
    'X': songs_principle[:,0],
    'Y': songs_principle[:,1],
    'cluster': labeled_songs['label'],
})

# Retrieve the 5 closest points to the median features of the playlist
similar_songs = get_closest_pts(cluster).reset_index()
list_of_songs = list(similar_songs['track_id'])
print(list_of_songs)
