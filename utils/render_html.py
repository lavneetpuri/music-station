import urllib.parse
from IPython.core.display import HTML
from models.playlist import PlayList

style_body = """
html, body {
  margin: 0;
}
.playlists-container {
  display: grid;
  grid-template-columns: repeat({num_playlists}, 1fr);
  grid-template-rows: auto;
  column-gap: 12px;
  font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;
}
.header {
  color: #333;
  text-align: center;
  margin: 14px 0 !important;
}
.notfound {
  background: #f5f5f5;
  border: 1px solid #e5e5e5;
  border-radius: 3px;
  box-sizing: border-box;
  padding: 10px;
  height: {not_found_height}px;
  margin-top: -6px;
  font-weight: 100;
}
.notfound .info {
  font-size: 12px;
  color: #666;
  float: right;
}
.notfound .artist {
  color: #666;
  font-size: 15px;
  text-decoration: underline;
}
.notfound .title {
  color: #333;
  font-size: 20px;
}
""".replace('{\n', '{{').replace('}\n', '}}').replace('\n','')

# returns the html with side-by-side rendered playlists
# pass a list of PlayList objects
def build_frame(playlists):
    html_body = ""
    song_frame_height = 110
    for plist in playlists:
        if not isinstance(plist, PlayList):
            raise TypeError('List values must be of type PlayList')

        html_body += render_playlist(plist, song_frame_height)
    
    frame = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Playlists</title>
        <style>
            {
                style_body.format(
                    num_playlists=len(playlists),
                    not_found_height=0.8 * song_frame_height
                )
            }
        </style>
    </head>
    <body><div class="playlists-container">{html_body}</div></body>
    </html>
    """.replace('\n', '')
    return HTML(frame)

# returns html structure of the given playlist 
def render_playlist(playlist, song_frame_height=110):
    player_url = 'https://w.soundcloud.com/player'
    playlist_body = f"""
    <header><h2 class="header">{playlist.name}</h2></header>
    """
    for song in playlist.songs:
        if song.uri:
            song_body = f"""
            <iframe width="100%" height="{song_frame_height}" frameborder="no" src="{player_url}/?url={urllib.parse.quote(song.uri)}">
            </iframe>
            """
        else:
            song_body = f"""
            <div class="notfound">
                <div class="info">&#9432; Audio Not Found</div>
                <a class="artist">{song.artist}</a><br>
                <span class="title">{song.name}</span>
            </div>
            """
        playlist_body += song_body
    
    return f"""
    <div class="playlist">{playlist_body}</div>
    """
