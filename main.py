from flask import Flask, render_template, request
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import datastore
from models.team import Team

app = Flask(__name__)
firebase_request_adapter = requests.Request()


@app.route('/')
def root():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)

    return render_template('index.html', user=claims, error_message=error_message)


@app.route('/add_team', methods=['POST'])
def addTeam():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            year_founded = request.form['year_founded']
            total_p_pos = request.form['total_p_pos']
            total_race_w = request.form['total_race_w']
            total_c_titles = request.form['total_c_titles']
            prevSeason_pos = request.form['prevSeason_pos']
        except ValueError as exc:
                
                error_message = str(exc)

    return render_template('index.html', user=claims, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
