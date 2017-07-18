import logging
import os

from flask_oauthlib.client import OAuth, OAuthException
from flask import Blueprint, redirect, url_for, request, session, current_app, render_template

from app.services.spotify_service import SpotifyService
from app.services.create_user_service import CreateUserService
from app.services.create_token_service import CreateTokenService
from app.services.create_playlist_service import CreatePlaylistService
from app.finders.user_finder import UserFinder

log = logging.getLogger(__name__)

spotify_bp = Blueprint('spotify', __name__, template_folder='/templates')

oauth = OAuth(current_app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=os.environ.get('CLIENT_ID', 'whatda'),
    consumer_secret=os.environ.get('CLIENT_SECRET', 'whatda'),
    request_token_params={'scope': 'playlist-read-private playlist-read-collaborative'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)


@spotify_bp.route('/')
def index():
    return redirect(url_for('spotify.login'))


@spotify_bp.route('/login')
def login():
    callback = url_for(
        'spotify.spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)


@spotify_bp.route('/login/authorized')
def spotify_authorized():
    response = spotify.authorized_response()
    if response is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(response, OAuthException):
        return 'Access denied: {0}'.format(response.message)

    session['oauth_token'] = (response['access_token'], '')

    spotify_service = SpotifyService(response['access_token'])
    me = spotify_service.me()

    user = UserFinder.get_from_spotify_id(me['id'])
    if not user:
        create_user_service = CreateUserService(me['display_name'], me['email'], me['id'])
        user = create_user_service.call()

        create_token_service = CreateTokenService(response['access_token'], response['token_type'], response['scope'],
                                                  response['expires_in'], response['refresh_token'], user.id)
        token = create_token_service.call()

    discover_weekly_playlist_meta_info = spotify_service.get_playlist(user.spotify_id, "Discover Weekly")
    discover_weekly_playlist = spotify_service.discover_weekly_playlist(discover_weekly_playlist_meta_info['id'])

    create_playlist_service = CreatePlaylistService(
        discover_weekly_playlist['id'],
        discover_weekly_playlist['tracks']['items'][0]['added_at'],
        user.id
    )
    playlist = create_playlist_service.call()

    return render_template('playlist.html', playlist=playlist)


@spotify_bp.route('/playlist')
def playlist():
    return render_template('playlist.html')


def get_spotify_oauth_token():
    return session.get('oauth_token')
