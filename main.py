import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import sys

# Spotify API Setup
spotify_client_id = 'YOUR_SPOTIFY_CLIENT_ID'
spotify_client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))

# YouTube API Setup
youtube_api_key = 'YOUR_YOUTUBE_API_KEY'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)


def get_spotify_track_info(spotify_url):
    track_id = sp.track(spotify_url)['id']
    track_info = sp.track(track_id)
    return {
        'name': track_info['name'],
        'artists': [artist['name'] for artist in track_info['artists']]
    }

def search_youtube_video(track_info):
    search_query = f"{track_info['name']} {track_info['artists'][0]} official video"
    request = youtube.search().list(q=search_query, part='snippet', type='video', maxResults=1)
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"

if __name__ == "__main__":
    spotify_link = sys.argv[1]
    if "open.spotify.com" in spotify_link:
        print(search_youtube_video(get_spotify_track_info(spotify_link)))
    else:
        print("Link must contain open.spotify.com")
        sys.exit()