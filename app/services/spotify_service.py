import requests
import os

from requests.auth import HTTPBasicAuth

from app.finders.user_finder import UserFinder


class SpotifyService:
    base_url = 'https://api.spotify.com/v1'

    def __init__(self, access_token):
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }

    def me(self):
        endpoint = self.base_url + '/me'

        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_playlist(self, user_id, name):
        endpoint = self.base_url + '/users/{}/playlists'.format(user_id)

        response = requests.get(endpoint, headers=self.headers)
        data = response.json()

        if response.status_code == 200:
            for playlist in data['items']:
                if playlist['name'] == name:
                    return playlist

        if response.status_code == 401 and data['error']['message'] == 'The access token expired':
            self._renew_access_token(user_id)

        return None

    def discover_weekly_playlist(self, playlist_id):
        endpoint = self.base_url + '/users/spotify/playlists/{}'.format(playlist_id)

        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()

        return None

    def _renew_access_token(self, user_id):
        endpoint = 'https://accounts.spotify.com/api/token'
        user = UserFinder.get_from_spotify_id(user_id)

        if user:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": user.token.refresh_token
            }

            response = requests.post(
                endpoint,
                auth=HTTPBasicAuth(os.environ.get('CLIENT_ID'), os.environ.get('CLIENT_SECRET')),
                data=data
            )
            data = response.json()

            if data.get('access_token'):
                user.token.access_token = data['access_token']
                user.token.save()

        return None
