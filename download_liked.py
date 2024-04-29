import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp

music_folder = os.path.join(os.path.expanduser("~"), "Music", "Liked")

scope = "user-library-read,playlist-modify-private,playlist-modify-public,user-library-modify"
id_type = "playlist"
playlist_id = "6ardHkqB8ZOoa6F8zPNDR2"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
    )
)

if id_type == "playlist":
    i = 50
    tracks = sp.current_user_saved_tracks(limit=50)
    while i < tracks["total"]:
        tracks["items"].extend(sp.current_user_saved_tracks(limit=50,offset=i)["items"])
        i += 50

elif id_type == "album":
    tracks = sp.album_tracks(playlist_id)

i = 0

for track in tracks["items"]:
    if id_type == "playlist":
        track = track["track"]
    """print("yt-dlp " +
            "-x " +
            "--audio-format mp3 " +
            f"--output \"{track["artists"][0]["name"]} - {track["name"]}\" "
            "--add-metadata " +
            "--postprocessor-args \"Metadata: " +
            f"-metadata track={track['track_number']}/{track['album']['total_tracks']} " +
            f"-metadata artist={'; '.join([artist['name'] for artist in track['artists']])} " +
            f"-metadata year={track['album']['release_date'][:4]} " + 
            f"-metadata title={track['name']} -metadata album={track['album']['name']}\" " +
            f"\"ytsearch:{track["artists"][0]["name"]} - {track["name"]}\""
    )"""

    filename = f"{track["artists"][0]["name"]} - {track["name"]}.mp3".replace("/", "\\")
    track_number = f"{track['track_number']}/{track['album']['total_tracks']}"
    artists = [artist['name'] for artist in track['artists']]
    help_me = '; '.join(artists)
    album = track['album']['name']
    title = track["name"]
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        ],
        'outtmpl': f"{artists[0]} - {title}"
    }
    path = os.path.join(music_folder, filename)
    if not os.path.exists(path):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f"ytsearch:{filename}"])
            except:
                pass

    """
    if not os.path.exists(f"{filename}.mp3") and "x0o0x" not in filename:
        print(
            "yt-dlp " +
                "-x " +
                "--audio-format mp3 " +
                f"--output \"{filename}\" "
                "--add-metadata " +
                "--postprocessor-args \"Metadata: " +
                f"-metadata track={track_number} " +
                f"-metadata artist='{'; '.join(artists)}' " +
                f"-metadata year={track['album']['release_date'][:4]} " + 
                f"-metadata title='{title}' -metadata album='{track['album']['name']}'\" " +
                f"\"ytsearch:{filename}\""
        )
        print(filename)
        os.system(
            "yt-dlp " +
                "-x " +
                "--audio-format mp3 " +
                f"--output \"{filename}\" "
                "--add-metadata " +
                "--postprocessor-args \"Metadata: " +
                f"-metadata track={track_number} " +
                f"-metadata artist='{'; '.join(artists)}' " +
                f"-metadata year={track['album']['release_date'][:4]} " + 
                f"-metadata title='{title}' -metadata album='{album}'\" " +
                f"\"ytsearch:{filename}\""
        )"""
    i += 1
print(i)
