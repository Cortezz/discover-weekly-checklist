import logging
import os

from flask_oauthlib.client import OAuth, OAuthException
from flask import Blueprint, redirect, url_for, request, session, current_app, render_template

log = logging.getLogger(__name__)

spotify_bp = Blueprint('spotify', __name__, template_folder='/templates')

oauth = OAuth(current_app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=os.environ.get('CLIENT_ID'),
    consumer_secret=os.environ.get('CLIENT_SECRET'),
    request_token_params={'scope': 'playlist-read-private'},
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
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return redirect(url_for('spotify.playlist'))


@spotify_bp.route('/playlist')
def playlist():
    return render_template('playlist.html')

@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')