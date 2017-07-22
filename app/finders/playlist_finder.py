from app.models.playlist import Playlist


class PlaylistFinder(object):

    @classmethod
    def get_last_playlist_from_user_id(cls, user_id):
        return Playlist.query.filter_by(user_id=user_id).order_by(Playlist.date.desc()).first()
