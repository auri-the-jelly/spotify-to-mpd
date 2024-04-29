import spotipy
from spotipy.oauth2 import SpotifyOAuth

import mutagen
from mutagen.easyid3 import EasyID3
from urllib.request import urlopen
from mutagen.id3 import ID3, APIC

import os
import json

scope = "user-library-read,playlist-modify-private,playlist-modify-public,user-library-modify"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
    )
)

"""i = 50
liked = sp.current_user_saved_tracks(limit=50)
while i < liked["total"]:
    liked["items"].extend(sp.current_user_saved_tracks(limit=50, offset=i)["items"])
    i += 50"""



liked = sp.current_user_saved_tracks(limit=50)
i = 50
while i < liked["total"]:
    liked["items"].extend(sp.current_user_saved_tracks(limit=50,offset=i)["items"])
    i += 50

music_dir = os.path.join(os.path.expanduser("~"), "Music", "Liked")
tracks = os.listdir(music_dir)

for song in liked["items"]:
    try:
        song = song["track"]
        filename = f"{song["artists"][0]["name"]} - {song["name"]}.mp3"
        path = os.path.join(music_dir, filename)
        audio = ID3(path)
        tag = EasyID3(path)
        if "AronChupa" in filename:
            print("help")
        if (filename in tracks and "artist" not in tag.keys()) or (tag and 'APIC:Cover' not in audio.keys()):
            tag["albumartist"] = [artist["name"] for artist in song["album"]["artists"] if artist["name"] != "Various Artists"]
            tag["artist"] = [artist["name"] for artist in song["artists"]]
            tag["title"] = [song["name"]]
            tag["album"] = [song["album"]["name"]]
            if not tag["albumartist"]:
                tag.pop("albumartist")
            tag.save()
            albumart = urlopen(song["album"]["images"][0]["url"])

            audio['APIC'] = APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc=u'Cover',
                            data=albumart.read()
                            )

            albumart.close()
            audio.save()
    except:
        pass
"""for track in tracks:
    try:
        if track != ".cache":
            path = os.path.join(music_dir, track)
            audio = ID3(path)
            tag = EasyID3(path)
            if tag and 'APIC:Cover' not in audio.keys():
                result = sp.search(f"track:{tag["title"]} artist:{tag["artist"][0]}")
                if result["tracks"]["items"]:
                    albumart = urlopen(result["tracks"]["items"][0]["album"]["images"][0]["url"])

                    audio['APIC'] = APIC(
                                    encoding=3,
                                    mime='image/jpeg',
                                    type=3,
                                    desc=u'Cover',
                                    data=albumart.read()
                                    )

                    albumart.close()
                    audio.save()
    except: 
        pass"""

"""tag = EasyID3(path)
if tag and "date" not in tag.keys():
    result = sp.search(f"track:{tag["title"]} artist:{tag["artist"][0]}")
    if result["tracks"]["items"]:
        tag["albumartist"] = [artist["name"] for artist in result['tracks']['items'][0]["album"]["artists"] if artist["name"] != "Various Artists"]
        if not tag["albumartist"]:
            tag.pop("albumartist")
        tag["date"] = [result["tracks"]["items"][0]["album"]["release_date"].replace("-", "")]
        tag.save()"""
