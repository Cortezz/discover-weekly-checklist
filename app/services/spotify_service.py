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