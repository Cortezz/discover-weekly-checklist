from app.database import db
from app.models.playlist import Playlist


class CreatePlaylistService(object):

    def __init__(self, spotfiy_id, date, user_id):
        self.spotify_id = spotfiy_id
        self.date = date
        self.user_id = user_id

    def call(self):
        playlist = Playlist(spotify_id=self.spotify_id, date=self.date, user_id=self.user_id)

        db.session.add(playlist)
        db.session.commit()
        db.session.refresh(playlist)

        return playlist
