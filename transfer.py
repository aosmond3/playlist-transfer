import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from googleapiclient.discovery import build

scope = 'playlist-modify-public'
username = '' #ADD SPOTIFY USERNAME

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

#create the playlist
playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
print()

spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

#get the songs
api_key = '' #ADD YOUTUBE API KEY
youtube = build('youtube', 'v3', developerKey=api_key)

song_dict = {}
nextPageToken = None #nextPageToken serves as a pointer, kinda, to the next page of results in a playlist
while True:
    playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId='', #ADD YOUTUBE PLAYLIST ID
            maxResults=50, #the max number of items that can be retrieved at once is 50
            pageToken=nextPageToken
        )
    playlist_response = playlist_request.execute()

    list_of_video_ids = []
    for video in playlist_response['items']:
        video_id = video['contentDetails']['videoId']
        list_of_video_ids.append(video_id)
    #now we have the first 50 video ids

    #gets a string of comma separated video id values
    query_string = ','.join(list_of_video_ids)

    video_request = youtube.videos().list(
            part='snippet',
            id=query_string
        )
    video_response = video_request.execute()

    for item in video_response['items']:
        title = item['snippet']['title']

        if 'tags' in item['snippet']:
            artist = item['snippet']['tags'][0]
        else:
            artist = ""

        song_dict.update({title : artist})

    nextPageToken = playlist_response.get('nextPageToken') #returns None if no more pages
    if not nextPageToken:
        break

num_songs_added = 0
list_of_songs = []
list_of_songs_not_found = []
num = 1
for song_title, artist in song_dict.items():
#for song_title in titles:
    result = spotifyObject.search(q=song_title + " " + artist)
    list_of_possible_songs = result['tracks']['items']
    if not list_of_possible_songs == []:
        print(f"Song title {num}: {song_title}")
        list_of_songs.append(list_of_possible_songs[0]['uri']) #get the song uri of the first search result and append it to the list of songs
        num_songs_added += 1
    else: #no search results (song not found)
        list_of_songs_not_found.append(song_title)
    num += 1

#find the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id'] #0 is to get the most recently added playlist

#add songs to playlist (can only do 100 at a time)
while not len(list_of_songs) == 0:
    spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs[0:99])
    del list_of_songs[0:99]

print(f"\n\n{num_songs_added} out of {len(song_dict)} songs were added to your new playlist.\n\n")
print("Songs not added:\n")
for song_title in list_of_songs_not_found:
    print(song_title)
print()
