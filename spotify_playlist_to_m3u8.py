import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

playlist_dir = os.path.join(os.path.expanduser("~"), ".mpd", "playlists")
music_dir = os.path.join(os.path.expanduser("~"), "Music", "Liked")


scope = "user-library-read,playlist-modify-private,playlist-modify-public,user-library-modify"
playlist_id = "1HdQmxpZ3dDkexpLkJTjD9"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
    )
)

i = 100
tracks = sp.playlist_tracks(playlist_id, limit=100)
while i < tracks["total"]:
    tracks["items"].extend(
        sp.playlist_tracks(playlist_id, limit=100, offset=i)["items"]
    )
    i += 100

m3u = ""
for track in tracks["items"]:
    track = track["track"]
    filename = f"{track["artists"][0]["name"]} - {track["name"]}.mp3"
    if filename in os.listdir(music_dir):
        m3u += f"Liked/{filename}\n"

with open(os.path.join(playlist_dir, "Best of Attack on Titan.m3u"), "w") as playlist:
    playlist.write(m3u)
