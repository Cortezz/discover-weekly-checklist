from app.services.create_song_service import CreateSongService


class CreatePlaylistSongsService(object):

    def __init__(self, spotfiy_weekly_playlist_json, playlist_id):
        self.spotify_weekly_playlist_json = spotfiy_weekly_playlist_json
        self.playlist_id = playlist_id

    def call(self):

        for song in self.spotify_weekly_playlist_json['tracks']['items']:
            artists = ""
            for artist in song['artists']:
                if not artists:
                    artists = artist
                else:
                    artists += ", {}".format(artists)
                create_song_service = CreateSongService(artists, song['name'], self.playlist_id)
                create_song_service.call()
