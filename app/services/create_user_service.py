from app.models.user import User
from app.database import db


class CreateUserService(object):

    def __init__(self, name, email, spotify_id):
        self.name = name
        self.email = email
        self.spotify_id = spotify_id

    def call(self):
        user = User(name=self.name, email=self.email, spotify_id=self.spotify_id)

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return user
