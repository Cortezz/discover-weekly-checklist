from app.database import db
from app.models.token import Token


class CreateTokenService(object):

    def __init__(self, access_token, token_type, scope, expires_in, refresh_token, user_id):
        self.access_token = access_token
        self.token_type = token_type
        self.scope = scope
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.user_id = user_id

    def call(self):
        token = Token(
            access_token=self.access_token,
            token_type=self.token_type,
            scope=self.scope,
            expires_in=self.expires_in,
            refresh_token=self.refresh_token,
            user_id=self.user_id
        )

        db.session.add(token)
        db.session.commit()
        db.session.refresh(token)

        return token
