/* Returns the artist id and a list of terms associated with them */
SELECT artist_id, group_concat(term, '|') AS terms, count(artist_id) 
AS num_terms FROM artist_term GROUP BY artist_id;

/* Returns the artist id and a list of musicbrainz tags associated with them */
SELECT artist_id, group_concat(mbtag, '|') AS tags, count(artist_id) 
AS num_tags FROM artist_mbtag GROUP BY artist_id;

/* Returns the artist id and a list of artist ids that are similar to the target */
SELECT target as target_artists, group_concat(similar, '|') AS similar_artists, 
count(target) AS num_artists FROM similarity GROUP BY target;

/* Combined the three tables into one single query to be outputted to csv with SQLite3 */
SELECT track_id, song_id, title, artist_name, duration, year, artist_mbid, 
songs.artist_id, tags as artist_tags, num_tags, terms as artist_terms, num_terms, similar_artists, 
num_artists, artist_hotttnesss AS artist_hotness, artist_familiarity FROM songs 
LEFT JOIN artist_mbtags ON songs.artist_id = artist_mbtags.artist_id 
LEFT JOIN artist_terms ON artist_terms.artist_id = songs.artist_id 
LEFT JOIN artist_similar ON artist_similar.target_artist = songs.artist_id;