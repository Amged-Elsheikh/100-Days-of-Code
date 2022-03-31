# %%
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
load_dotenv()


class Spotify_API:
    spotify_auth_url = "http://127.0.0.1:8080"

    def __init__(self, scope="playlist-modify-private"):
        self.scope = scope
        username = os.environ.get('SPOTIFY_USERNAME')

        # Get the Token
        self._token = SpotifyOAuth(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                   client_secret=os.environ.get(
                                       'SPOTIPY_CLIENT_SECRET'),
                                   scope=self.scope,
                                   redirect_uri=self.spotify_auth_url,
                                   username=username,
                                   cache_path="token.txt")
        # Initialize the client
        self._sp = spotipy.Spotify(auth_manager=self._token)
        # Cache the Token to the system
        self._sp.current_user()

    def search(self, top_hits):
        hits_uri = []
        not_found = 0
        for hit in top_hits:
            try:
                hits_uri.append(self._sp.search(q=f"track:{hit}", market="US")[
                    'tracks']['items'][0]["uri"])
            except:
                # If song not found
                print(f"'{hit}' is not in Spotify.😔")
                not_found += 1
        if not_found:
            print(f"Could not find {not_found} hit(s) in Spotify")
        else:
            print("All track found in Spotify")
        return hits_uri

    def create_playlist(self, name, public=False):
        playlist = self._sp.user_playlist_create(user=self._sp.current_user()['id'],
                                                 name=name, public=public)
        return playlist

    def add_song_to_playlist(self, playlist, tracks_uri):
        self._sp.playlist_add_items(
            playlist_id=playlist["id"], items=tracks_uri)


def get_top_hits(date: str):
    url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(f"{url}/{date}")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.select(
        ".chart-results-list .o-chart-results-list-row-container h3")
    top_hits = [data[i].text.strip() for i in range(0, len(data), 4)]
    return top_hits


if __name__ == "__main__":
    sp = Spotify_API()
    
    year = input("Enter the year of the hits: ")
    month = input("Enter the month of the hits in 'XX' format: ")
    day = input("Enter the day of the hits in 'XX' format: ")
    date = f"{year}-{month}-{day}"

    top_hits = get_top_hits(date)
    hits_uri = sp.search()
    
    playlist = sp.create_playlist(name=f"{date} Top Hits")
    print(f"'{date} Top Hits' playlist is created")

    # Add tracks to the new playlist
    sp.add_song_to_playlist(playlist=playlist, tracks_uri=hits_uri)
