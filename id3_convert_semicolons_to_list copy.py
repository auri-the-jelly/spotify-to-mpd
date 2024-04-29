import mutagen
from mutagen.easyid3 import EasyID3
import os

music_dir = os.path.join(os.path.expanduser("~"), "Music", "Liked")
for track in os.listdir(music_dir):
    path = os.path.join(music_dir, track)
    try:
        tag = EasyID3(path)
    except:
        if track != ".cache":
            tag = mutagen.File(path, easy=True)
            tag.add_tags()
    try:
        if ";" in tag["artist"][0]:
            values = tag["artist"][0].split(";")
            values = [value.strip() for value in values]
            tag["artist"] = values
            print(tag["artist"])
            tag.save(v2_version=4)
            """values = "|".join(tag["artist"][0].split(";"))
            tag["artist"] = [values]
            print(tag["artist"])
            tag.save(v2_version=3)"""
    except:
        pass
