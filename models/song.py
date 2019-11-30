from data.main import songs
from data.main import artists
from api.main import SoundCloudAPI as API

class Song:
    def __init__(self, track_id):
        track = songs[songs.track_id == track_id]
        if track.empty: raise ValueError(f'Unknown track id {track_id}')

        self.id = track_id
        self.name = track.title.values[0]

        artist_id = track.artist_id.values[0]
        artist = artists[artists.artist_id == artist_id]
        self.artist = artist.artist_name.values[0]

        try:
            metadata = API.song_metadata(f'{self.name} - {self.artist}')
        except Warning:
            metadata = {}

        self.uri = metadata.get('uri')
