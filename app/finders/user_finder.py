from app.models.user import User


class UserFinder(object):

    @classmethod
    def get_from_spotify_id(cls, spotify_id):
        return User.query.filter_by(spotify_id=spotify_id).first()

    @classmethod
    def get_from_id(cls, user_id):
        return User.query.get(user_id)
