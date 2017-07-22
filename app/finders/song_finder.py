from app.models.song import Song


class SongFinder(object):

    @classmethod
    def get_from_id(cls, song_id):
        return Song.query.get(song_id)

    @classmethod
    def get_playlist_songs_from_status(self, playlist_id, status):
        return Song.query.filter_by(playlist_id=playlist_id, status=status).all()
