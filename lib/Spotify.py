# This Python file uses the following encoding: utf-8
import json
import requests

class Spotify():
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {"Authorization": "Bearer " + self.access_token}

    def getCategories(self):
        url = "https://api.spotify.com/v1/browse/categories"
        categories = requests.get(url, headers=self.headers)
        return json.loads(categories.content)["categories"]["items"]

    def getCategoryPlaylists(self, id):
        url = "https://api.spotify.com/v1/browse/categories/{category_id}/playlists".format(category_id=id)
        playlists = requests.get(url, headers=self.headers)
        return json.loads(playlists.content)["playlists"]["items"]
