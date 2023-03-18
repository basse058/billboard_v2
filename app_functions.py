# Glen dependencies
import pandas
import numpy as np
import request
import re
import joblib
from sklearn.svm import SVC 
import pickle
# Import dependencies for Spotipy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Import Client ID and Client Secret
from config import cid, secret


@app.route("/use_model/<feature:track_features>&<decade:decade")
def predict_track(track_features, decade):
    if not 'track_features' in request.args:
        return "Track features are missing"
    if not 'decade' in request.args:
        return "Select a decade"
    
    file_path = "./ML_models/"
    model_names = {"1960s": "model_1960s",
                "1970s": "model_1970s",
                "1980s": "model_1980s",
                "1990s": "model_1990s",
                "2000s": "model_2000s",
                "2010s": "model_1970s"}
    
    scaler_names = {"1960s": "scaler_1960s",
                "1970s": "scaler_1970s",
                "1980s": "scaler_1980s",
                "1990s": "scaler_1990s",
                "2000s": "scaler_2000s",
                "2010s": "scaler_2010s"}

    # load model
    loaded_model = joblib.load(f"{file_path}{model_names[decade]}")
    loaded_scaler = joblib.load(f"{file_path}{scaler_names[decade]}")

    scaled_features = loaded_scaler.transform(track_features)

    # you can use loaded model to compute predictions
    y_predict = loaded_model.predict(scaled_features)
    y_pred_proba = loaded_model.predict_proba(scaled_features)

    if y_predict[0] == 1:
        billboard_prob = round(y_pred_proba[0][0], 3) * 100
        noncharting_prob = round(y_pred_proba[0][1],3) * 100
    else:
        billboard_prob = round(y_pred_proba[0][1], 3) * 100
        noncharting_prob = round(y_pred_proba[0][0],3) * 100

    return billboard_prob, noncharting_prob


# SPOTIFY API
# Create objects for accessing Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_spotify(song_title, artist):
    try:
        searchResults = sp.search(q=f"artist:{artist} track:{song_title}", type="track")
        track_id = searchResults['tracks']['items'][0]['id']

        return track_id
    except:
        pass

def adjust_parens(song_title):
    combinations = []

    strip_parens = ' '.join(song_title.strip(')(').split(')'))
    strip_parens = ' '.join(strip_parens.strip(' (').split('(')).replace('  ',' ')
    combinations.append(strip_parens)

    try:
        inside_parens = re.findall(r'\(.*?\)', song_title)[0].strip('()').strip()
    except IndexError:
        pass
        
    try:
        left_parens = song_title.split(f"({inside_parens})")[0].strip()
        if (left_parens not in combinations) & (len(left_parens) > 0): 
            combinations.append(left_parens)
    except:
        left_parens = "NA"

    try:
        right_parens = song_title.split(f"({inside_parens})")[1].strip()
        if (right_parens not in combinations) & (len(right_parens) > 0): 
            combinations.append(right_parens)
    except:
        right_parens = "NA"

    return combinations

# Create function to retrieve track ID from Spotify given the artist and song title
@app.route("/search_spotify/track=<song_title>&artist=<artist>")
def get_track_features(song_title, artist):
    while True:
        # Select first artist if multiple listed with "Featuring" keyword
        if 'Featuring' in artist:
            artist = artist.split(' Featuring ')[0]
        # Select first artist if multiple listed with "with", "With", or "," substrings
        elif ' with ' in artist:
            artist = artist.split(' with ')[0]
        elif ' With ' in artist:
            artist = artist.split(' With ')[0]
        elif "," in artist:
            artist = artist.split(',')[0]

        # Make initial API search, return ID string if found
        found_id = search_spotify(song_title, artist)
        if found_id:

            return get_audio_features(found_id)

        # Search artist and song title (replacing words ending in "in" to "ing")
        song_title = re.sub(r"in\b", 'ing ', song_title)
        found_id = search_spotify(song_title, artist)
        if found_id:
            return get_audio_features(found_id)

        if '(' in song_title:
            for item in adjust_parens(song_title):
                found_id = search_spotify(item, artist)
                if found_id:
                    return get_audio_features(found_id)
                
        # Check for '/' character in song_title
        if '/' in song_title:
            # Try string on left side of '/'
            song_title = song_title.split('/')[0]
            found_id = search_spotify(song_title, artist)
            if found_id:
                return get_audio_features(found_id)

            # Try string on right side of '/'
            try:
                song_title = song_title.split('/')[1]
                found_id = search_spotify(song_title, artist)
                if found_id:
                    return get_audio_features(found_id)
            except:
                pass

        # Check for '&' character in artist name
        if ' & ' in artist:
            artist = artist.split(' & ')[0]
            found_id = search_spotify(song_title, artist)
            if found_id:
                return get_audio_features(found_id)
        # Check for 'X' character in artist name
        if ' X ' in artist:
            artist = artist.split(' X ')[0]
            found_id = search_spotify(song_title, artist)
            if found_id:
                return get_audio_features(found_id)
        # Check for 'x' character in artist name
        if ' x ' in artist:
            artist = artist.split(' x ')[0]
            found_id = search_spotify(song_title, artist)
            if found_id:
                return get_audio_features(found_id)
            
        # Print song title and artist for non-match
        if found_id:
            return get_audio_features(found_id)
        
        break

            # print(f"No ID found for '{song_title}' by {artist}")
# Returns tuple of audio features from Spotify for specified track_id
def get_audio_features(id):
    try:
        search_results = sp.audio_features(id)[0]
        danceability = search_results['danceability']
        energy = search_results['energy']
        # key = search_results['key']
        loudness = search_results['loudness']
        # mode = search_results['mode']
        speechiness = search_results['speechiness']
        acousticness = search_results['acousticness']
        instrumentalness = search_results['instrumentalness']
        liveness = search_results['liveness']
        valence = search_results['valence']
        tempo = search_results['tempo']
        duration_ms = search_results['duration_ms']
        # time_signature = search_results['time_signature']
    except:
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

    return [danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, \
                valence, tempo, duration_ms]