import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

import flask_cors
from flask_cors import CORS, cross_origin

import joblib
from sklearn.svm import SVC 
import pickle

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///billboard.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
bbaf = Base.classes.all_songs_final

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#################################################
# Flask Routes
#################################################

@app.route("/")
@cross_origin()

def index():
    return render_template('index.html')

def welcome():
    """It worked! List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/billboard_features"
    )


@app.route("/api/v1.0/billboard_features")
def data():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(bbaf.song, bbaf.artist, bbaf.year, bbaf.peak_rank, bbaf.weeks_on_board, bbaf.track_id, bbaf.danceability, bbaf.energy, bbaf.key, bbaf.loudness, bbaf.mode, bbaf.speechiness, bbaf.instrumentalness, bbaf.liveness, bbaf.valence, bbaf.tempo, bbaf.duration_ms, bbaf.time_signature, bbaf.billboard, bbaf.decade).all()

    session.close()


    # Create a dictionary from the row data and append to a list of all_passengers
    all_features = []
    for song, artist, year, peak_rank, weeks_on_board, track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature, billboard, decade in results:
        features_dict = {}

        features_dict["song"] = song
        features_dict["artist"] = artist
        features_dict["year"] = year
        features_dict["peak_rank"] = peak_rank
        features_dict["weeks_on_board"] = weeks_on_board
        features_dict["track_id"] = track_id
        features_dict["danceability"] = danceability
        features_dict["energy"] = energy
        features_dict["key"] = key
        features_dict["loudness"] = loudness
        features_dict["mode"] = mode
        features_dict["speechiness"] = speechiness
        features_dict["acousticness"] = acousticness
        features_dict["instrumentalness"] = instrumentalness
        features_dict["liveness"] = liveness
        features_dict["valence"] = valence
        features_dict["tempo"] = tempo
        features_dict["duration_ms"] = duration_ms
        features_dict["time_signature"] = time_signature
        features_dict["billboard"] = billboard
        features_dict["decade"] = decade

        all_features.append(features_dict)

    return jsonify(all_features)

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




if __name__ == '__main__':
    app.run()
