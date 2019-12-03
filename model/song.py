from data.main import songs
from data.main import artists
from api.main import SoundCloudAPI as API

class Song:
    def __init__(self, track_id):
        track = songs.loc[track_id]
        if track.empty: raise ValueError(f'Unknown track id {track_id}')

        self.id = track_id
        self.name = track.title

        artist = artists.loc[track.artist_id]
        self.artist = artist.artist_name

        try:
            metadata = API.song_metadata(f'{self.name} - {self.artist}')
        except Warning:
            metadata = {}

        self.uri = metadata.get('uri')
