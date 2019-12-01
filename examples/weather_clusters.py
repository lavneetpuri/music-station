#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def get_pca(X):
    """
    Transform data to 2D points for plotting. Should return an array with shape (n, 2).
    """
    flatten_model = make_pipeline(
        MinMaxScaler(),
        PCA(2)
    )
    X2 = flatten_model.fit_transform(X)
    assert X2.shape == (X.shape[0], 2)
    return X2


def get_clusters(X):
    """
    Find clusters of the weather data.
    """
    model = make_pipeline(
        MinMaxScaler(),
        KMeans(n_clusters=10)
    )
    model.fit(X)
    return model.predict(X)

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


def main():
    data = pd.read_csv(sys.argv[1])

    X = data.loc[:,'tmax-01':'snwd-12']
    Y = data['city']

    # This contains the X and Y coords
    X2 = get_pca(X)

    # This contains the cluster classification
    clusters = get_clusters(X)

    plt.scatter(X2[:, 0], X2[:, 1], c=clusters, cmap='Set1', edgecolor='k', s=20)
    # plt.savefig('clusters.png')

    df = pd.DataFrame({
        'X': X2[:,0],
        'Y': X2[:,1],
        'cluster': clusters,
        'city': Y,
    })

    closest_pts = get_closest_pts(df)
    print(closest_pts)

    # counts = pd.crosstab(df['city'], df['cluster'])
    # print(counts)


if __name__ == '__main__':
    main()
