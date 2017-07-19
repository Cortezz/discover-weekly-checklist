import requests


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

        if response.status_code == 200:
            playlist = response.json()
            for playlist in playlist['items']:
                if playlist['name'] == name:
                    return playlist

        return None

    def discover_weekly_playlist(self, playlist_id):
        endpoint = self.base_url + '/users/spotify/playlists/{}'.format(playlist_id)

        response = requests.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            return response.json()

        return None
