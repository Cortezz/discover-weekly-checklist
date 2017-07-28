import logging
import os
import datetime
import json
import arrow

from flask_oauthlib.client import OAuth, OAuthException
from flask import Blueprint, redirect, url_for, request, session, current_app, render_template, Response
from flask_login import login_user, login_required, current_user, logout_user


from app.services.spotify_service import SpotifyService
from app.services.create_user_service import CreateUserService
from app.services.create_token_service import CreateTokenService
from app.services.create_playlist_songs_service import CreatePlaylistSongsService
from app.services.create_playlist_service import CreatePlaylistService
from app.finders.user_finder import UserFinder
from app.finders.playlist_finder import PlaylistFinder
from app.finders.song_finder import SongFinder

log = logging.getLogger(__name__)

discover_weekly = Blueprint('discover_weekly', __name__, template_folder='/templates')

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


@discover_weekly.route('/')
def home():
    if current_user.is_authenticated:
        redirect(url_for('discover_weekly.playlist'))
    else:
        return render_template('home.html')


@discover_weekly.route('/login', methods=['POST'])
def login():
    callback = url_for(
        'discover_weekly.spotify_authorized',
        _external=True
    )
    return spotify.authorize(callback=callback)


@discover_weekly.route('/login/authorized')
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

    login_user(user)

    return redirect(url_for('discover_weekly.playlist'))


@discover_weekly.route('/discover_weekly')
@login_required
def playlist():
    discover_weekly_playlist = PlaylistFinder.get_last_playlist_from_user_id(current_user.id)

    if not discover_weekly_playlist or (datetime.datetime.utcnow() - discover_weekly_playlist.date).days >= 7:

        spotify_service = SpotifyService(current_user.token.access_token)
        discover_weekly_playlist_meta_info = spotify_service.get_playlist(current_user.spotify_id, "Discover Weekly")
        discover_weekly_playlist_json = spotify_service.discover_weekly_playlist(discover_weekly_playlist_meta_info['id'])

        create_playlist_service = CreatePlaylistService(
            discover_weekly_playlist_json['id'],
            discover_weekly_playlist_json['tracks']['items'][0]['added_at'],
            current_user.id
        )
        discover_weekly_playlist = create_playlist_service.call()

        create_playlist_songs_service = CreatePlaylistSongsService(discover_weekly_playlist_json,
                                                                   discover_weekly_playlist.id)
        create_playlist_songs_service.call()

    liked_songs = SongFinder.get_playlist_songs_from_status(discover_weekly_playlist.id, 'liked')
    normal_songs = SongFinder.get_playlist_songs_from_status(discover_weekly_playlist.id, 'normal')
    created_at_friendly = arrow.get(discover_weekly_playlist.created_at).humanize()

    return render_template('playlist.html', playlist=discover_weekly_playlist, created_at=created_at_friendly,
                           liked_songs_count=len(liked_songs), normal_songs_count=len(normal_songs),
                           discover_weekly_endpoint=os.environ.get('DISCOVER_WEEKLY_ENDPOINT'))


@discover_weekly.route('/songs/<song_id>/status', methods=['PUT'])
def update_status(song_id):
    song = SongFinder.get_from_id(song_id)

    if not song:
        return Response(
            response=json.dumps({"error": "Song not found"}),
            status=404,
            mimetype='application/json'
        )

    data = request.json
    new_song_status = data.get('status')
    if new_song_status not in ['normal', 'liked', 'removed']:
        return Response(
            response=json.dumps({"error": "Status value must be 'normal', 'liked' or 'removed'"}),
            status=400,
            mimetype='application/json'
        )

    song.status = new_song_status
    song.save()

    return Response(
        response=json.dumps({'status': 'success'}),
        status=200,
        mimetype='application/json'
    )


@discover_weekly.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('discover_weekly.home'))
