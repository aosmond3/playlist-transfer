# playlist-transfer
Transfers youtube music playlists to spotify.

transfer.py: a script to transfer a PUBLIC YouTube Music playlist into a Spotify playlist. 

# Set-up:

Initially, you should create a virtual environment within the source folder of your project. Do this with 'virtualenv <your-env>, assuming you already pip installed 'virtualenv'.

Next, activate the virtual environment with 'source <your-env>/bin/activate'

Next, pip install the needed apis:
  * Spotify:
    * pip install spotipy 
  * Youtube:
    * pip install google-api-python-client
	

Retrieve data needed from your Spotify and Google developer accounts and add them to the project:
  * Spotify:
    * export SPOTIPY_CLIENT_ID=
    * export SPOTIPY_CLIENT_SECRET=
    * export SPOTIPY_REDIRECT_URI=
    * note: need to configure the redirect uri in the settings of your Spotify developer account
  * Google:
    * add your api key to the script 
  
  Fill in the username, api_key, and playlistId variables in transfer.py
  

