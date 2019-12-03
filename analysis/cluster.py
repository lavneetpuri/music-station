from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from data.main import songs

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

# retuns original songs df with cluster labels
# new df may be smaller due to filtering of invalid rows
def get_labeled_songs(X, clusters, add_cols):
    labeled_songs = X.copy()
    labeled_songs['label'] = clusters
    for col_name in add_cols:
        labeled_songs[col_name] = songs[col_name]
    return labeled_songs


irrelevant_cols = ['title', 'artist_id']
# TODO: should these be included?
irrelevant_cols.extend(['end_of_fade_in', 'start_of_fade_out'])

filtered_songs = filter_songs(irrelevant_cols)
