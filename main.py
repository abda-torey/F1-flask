from flask import Flask, render_template, request, redirect, url_for
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import datastore


app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()


def create_team(name, year_founded, total_p_pos, total_race_w, total_c_titles, prevSeason_pos):
    entity_key = datastore_client.key('Teams')
    entity = datastore.Entity(key=entity_key)
    entity.update({
        'name': name,
        'year_founded': year_founded,
        'total_p_pos': total_p_pos,
        'total_race_w': total_race_w,
        'total_c_titles': total_c_titles,
        'prevSeason_pos': prevSeason_pos
    })
    datastore_client.put(entity)


def retrieveTeams():
    query = datastore_client.query(kind='Teams')
    teams = query.fetch()

    return teams


def retrieveDrivers():
    query = datastore_client.query(kind='Drivers')
    drivers = query.fetch()

    return drivers


def create_driver(name, age, pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, teamID, team_name):
    entity_key = datastore_client.key('Drivers')
    entity = datastore.Entity(key=entity_key)

    entity.update({
        'name': name,
        'age': age,
        'pole_positions': pole_positions,
        'total_race_wins': total_race_wins,
        'total_points_scored': total_points_scored,
        'total_world_titles': total_world_titles,
        'total_fastest_laps': total_fastest_laps,
        'teamID': teamID,
        'teamName': team_name

    })
    datastore_client.put(entity)


@app.route('/filter_drivers', methods=['POST'])
def filterDriver():
    result = None

    team = int(request.form['team'])
    wins = request.form['wins']
    query = datastore_client.query(kind='Drivers')
    if team:
        query.add_filter('teamID', '=', team)
    if wins:
        query.add_filter('total_race_wins', '>=', wins)

    drivers = query.fetch()

    teamNames = list(retrieveTeams())

    return render_template('driver.html', drivers=drivers, teamNames=teamNames)


@app.route('/filter_teams', methods=['POST'])
def filterTeams():
    total_c_titles = request.form['total_c_titles']

    query = datastore_client.query(kind='Teams')
    if total_c_titles:
        query.add_filter('total_c_titles', '>', total_c_titles)

    teamNames = query.fetch()

    return render_template('teams.html', teamNames=teamNames)


@app.route('/teams')
def teams():
    teamNames = retrieveTeams()

    return render_template('teams.html', teamNames=teamNames)


@app.route('/add_team', methods=['POST'])
def addTeam():

    name = request.form['name']
    year_founded = request.form['year_founded']
    total_p_pos = request.form['total_p_pos']
    total_race_w = request.form['total_race_w']
    total_c_titles = request.form['total_c_titles']
    prevSeason_pos = request.form['prevSeason_pos']
    create_team(name, year_founded, total_p_pos,
                total_race_w, total_c_titles, prevSeason_pos)
    return redirect(url_for('teams'))
    return render_template('teams.html')


@app.route('/drivers')
def drivers():
    teamNames = list(retrieveTeams())
    drivers = retrieveDrivers()

    return render_template('driver.html', teamNames=teamNames, drivers=drivers)


@app.route('/add_driver', methods=['POST'])
def addDriver():

    error_message = None
    teamNames = None
    team_name = None
    name = request.form['firstName']
    age = request.form['age']
    pole_positions = request.form['pole_positions']
    total_race_wins = request.form['total_race_wins']
    total_points_scored = request.form['total_points_scored']
    total_world_titles = request.form['total_world_titles']
    total_fastest_laps = request.form['total_fastest_laps']
    teamID = int(request.form['team'])
    teams = retrieveTeams()
    for team in teams:
        if team.key.id == teamID:
            team_name = team['name']
            break

    create_driver(name, age,
                  pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, teamID, team_name)

    return redirect(url_for('drivers'))

    return render_template('driver.html', teamNames=teamNames)


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

    print("claims:", claims)

    return render_template('base.html', user=claims, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
