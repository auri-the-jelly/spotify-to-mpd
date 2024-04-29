# spotify-to-mpd
Downloads and converts spotify liked songs and playlists to mp3 files and m3u playlists.

# Instructions
Just adjust the variables to your profile, set the variables SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI and run the files with `python file.py` 

`download_liked` downloads all liked songs.
`id3_add_extra_data` add the metadata for them
`spotify_playlist_to_m3u8` clones the spotify playlist into an mpd one