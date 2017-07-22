from app.models.song import Song


class SongFinder(object):

    @classmethod
    def get_from_id(cls, song_id):
        return Song.query.get(song_id)
