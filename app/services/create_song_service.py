from app.models.song import Song
from app.database import db


class CreateSongService(object):

    def __init__(self, artist, title, playlist_id):
        self.artist = artist
        self.title = title
        self.playlist_id = playlist_id

    def call(self):
        song = Song(artist=self.artist, title=self.title, playlist_id=self.playlist_id)

        db.session.add(song)
        db.session.commit()
        db.session.refresh(song)

        return song
