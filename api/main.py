import urllib.parse
import requests
import re

# return client_id for talking to SoundCloud API
def fetch_client_id():
    # url of script containing the client_id
    token_script_url = 'https://a-v2.sndcdn.com/assets/48-b4814ad6-3.js'
    req = requests.get(token_script_url)
    if req.status_code != 200:
        raise Warning(
            f'HTTP {req.status_code}: Unable to fetch client_id')

    id_pattern = re.compile('query:{client_id:"(.+?)"')
    matches = id_pattern.findall(req.content.decode('utf-8'))
    if len(matches) == 0:
        raise Warning('Missing Field: Unable to fetch client_id')

    return matches[0]

# Static class with helper methods for communicating with the soundcloud API
class SoundCloudAPI:
    try:
        CLIENT_ID = fetch_client_id()
    except Warning as w:
        print(w)
        CLIENT_ID = ''
    BASE_URL = 'https://api-v2.soundcloud.com'

    # query can be a combination of song name and artist
    # e.g. 'The Rolling Stones - Paint it black'
    @classmethod
    def song_metadata(cls, query):
        # search query is limited to only one result
        search_url = f'{cls.BASE_URL}/search/tracks?&q={urllib.parse.quote(query)}&limit=1&client_id={cls.CLIENT_ID}'
        req = requests.get(search_url)
        if req.status_code != 200:
            raise Warning(
                f'HTTP {req.status_code}: Unable to fetch song metadata')

        data = req.json()
        if not data['total_results']:
            return {}
        
        # return the top result
        return data['collection'][0]
