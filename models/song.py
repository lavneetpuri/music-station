from data.main import songs
from api.main import SoundCloudAPI as API

class Song:
    def __init__(self, track_id):
        track = songs[songs.track_id == track_id]
        if track.empty: raise ValueError(f'Unknown track id {track_id}')

        self.id = track_id
        self.name = track.title.values[0]
        # TODO: artist_name is not present in songs dataset
        # self.artist = track.artist_name.values[0]
        self.artist = 'Some Artist'

        try:
            metadata = API.song_metadata(self.name)
        except Warning:
            metadata = {}

        self.uri = metadata.get('uri')
