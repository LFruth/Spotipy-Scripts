import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = 'Client_ID'
CLIENT_SECRET = 'Client_Secret'


# Filter out non-unicode chars (e.g. emojis)
def BMP(s):
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

def encode_utf8_tostring(s):
    encoded = str(s.encode("utf-8"))
    result = encoded[2:-1]
    return result

# Returns name, artist and album of the given tracks
def get_tracks_infos(tracks):
    results = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        #print('%s, %s, %s' % (track_name, artist, album))

        result = track_name + ', ' + artist + ', ' + album
        results.append(result)
    return results
    
        
if __name__ == '__main__':
    # Login...
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print('Enter username:')
    username = input()
    
    print('Enter path to save lists to: ')
    path = input()
    
    playlists = sp.user_playlists(username)
    
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:

            # Get playlist infos...
            pl_name = BMP(playlist['name'])
            print('\n%s' % pl_name)

            results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
            tracks = results['tracks']

            # Get tracks from playlist
            pl_songs = get_tracks_infos(tracks)
            while(tracks['next']):
                tracks = sp.next(tracks)
                pl_songs.extend(get_tracks_infos(tracks))

            # Save playlist to .txt
            filepath = path + '/' + pl_name + '.txt'
            file = open(filepath, 'w+')
            for song in pl_songs:
                file.write(encode_utf8_tostring(song))
                file.write('\n')

            file.close()
