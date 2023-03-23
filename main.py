from flask import Flask, render_template, request, redirect, url_for
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import datastore
from models.team import Team
from models.driver import Driver


app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()


@app.route('/filter_drivers', methods=['POST'])
def filterDriver():

    team = request.form['team']
    wins = request.form['wins']
    query = datastore_client.query(kind='Drivers')
    # check for each filter attribute, if they exist, add filter to query
    if team:
        query.add_filter('teamName', '=', team)
    if wins:
        query.add_filter('total_race_wins', '>=', int(wins))

    drivers = query.fetch()

    teamNames = list(Team.retrieve_teams())
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('driver.html', user=claims, drivers=drivers, teamNames=teamNames)


@app.route('/filter_teams', methods=['POST'])
def filterTeams():
    total_c_titles = int(request.form['total_c_titles'])

    query = datastore_client.query(kind='Teams')
    if total_c_titles:
        query.add_filter('total_c_titles', '>=', total_c_titles)

    teamNames = query.fetch()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('teams.html', user=claims, teamNames=teamNames)


@app.route('/teams')
def teams():
    teamNames = Team.retrieve_teams()
    id_token = request.cookies.get("token")
    claims = None
    error = request.args.get('error')
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('teams.html', user=claims, teamNames=teamNames, error=error)


@app.route('/add_team', methods=['POST'])
def addTeam():

    error = None
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            name = request.form['name'].lower()
            year_founded = request.form['year_founded']
            total_p_pos = int(request.form['total_p_pos'])
            total_race_w = int(request.form['total_race_w'])
            total_c_titles = int(request.form['total_c_titles'])
            prevSeason_pos = int(request.form['prevSeason_pos'])
            try:
                Team.create_team(name, year_founded, total_p_pos,
                                 total_race_w, total_c_titles, prevSeason_pos)

            except ValueError as exc:
                error = str(exc)
        except ValueError as exc:
            error_message = str(exc)
    # using redirect to take the user to the new updated list of teams in the teams route
    return redirect(url_for('teams', error=error))


@app.route('/team_details/<string:name>')
def team_details(name):
    key = datastore_client.key('Teams', name)
    query = datastore_client.query(kind='Teams')
    query.add_filter('__key__', '=', key)
    teamDetails = query.fetch()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('teamPage.html', user=claims, teamDetails=teamDetails)


@app.route('/driver_details/<string:name>')
def driver_details(name):

    key = datastore_client.key('Drivers', name)
    query = datastore_client.query(kind='Drivers')
    query.add_filter('__key__', '=', key)
    driverDetails = query.fetch()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('driverPage.html', user=claims, driverDetails=driverDetails)

# we pass the name in the params because it acts as our key in the Entity Teams


@app.route('/editable_team/<string:name>')
def editable_team(name):
    key = datastore_client.key('Teams', name)
    query = datastore_client.query(kind='Teams')
    query.add_filter('__key__', '=', key)
    teamDetails = query.fetch()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('editTeam.html', user=claims, teamDetails=teamDetails)

# we pass the name in the params because it acts as our key in the Entity Drivers


@app.route('/editable_driver/<string:name>')
def editable_driver(name):
    key = datastore_client.key('Drivers', name)
    query = datastore_client.query(kind='Drivers')
    query.add_filter('__key__', '=', key)
    driverDetails = query.fetch()
    teamNames = Team.retrieveTeams()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('editDriver.html', user=claims, driverDetails=driverDetails, teamNames=teamNames)

# we pass the name in the params because it acts as our key in the Entity Teams


@app.route('/update_team/<string:name>', methods=['POST'])
def update_team(name):
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            name = request.form['name'].lower()
            year_founded = int(request.form['year_founded'])
            total_p_pos = int(request.form['total_p_pos'])
            total_race_w = int(request.form['total_race_w'])
            total_c_titles = int(request.form['total_c_titles'])
            prevSeason_pos = int(request.form['prevSeason_pos'])
            Team.update_team_details(name, year_founded, total_p_pos,
                                     total_race_w, total_c_titles, prevSeason_pos)
        except ValueError as exc:
            error_message = str(exc)

    return redirect(url_for('teams'))

# we pass the name in the params because it acts as our key in the Entity Drivers


@app.route('/update_driver/<string:name>', methods=['POST'])
def update_driver(name):
    teamNames = None
    team_name = None
    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        # convert the number values to int before saving to datastore
            name = request.form['firstName'].lower()
            age = int(request.form['age'])
            pole_positions = int(request.form['pole_positions'])
            total_race_wins = int(request.form['total_race_wins'])
            total_points_scored = int(request.form['total_points_scored'])
            total_world_titles = int(request.form['total_world_titles'])
            total_fastest_laps = int(request.form['total_fastest_laps'])
            team_name = request.form['team']

            Driver.update_driver(name, age,
                                 pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name)

        except ValueError as exc:
            error_message = str(exc)

    return redirect(url_for('drivers'))

# we pass the name in the params because it acts as our key in the Entity Teams


@app.route('/delete_team/<string:name>')
def delete_team(name):
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            Team.delete_team(name)
        except ValueError as exc:
            error_message = str(exc)

    return redirect(url_for('teams'))


@app.route('/delete_driver/<string:name>')
def delete_driver(name):
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            Driver.delete_driver(name)
        except ValueError as exc:
            error_message = str(exc)

    return redirect(url_for('drivers'))


@app.route('/drivers')
def drivers():
    teamNames = list(Team.retrieve_teams())
    drivers = Driver.retrieve_drivers()
    error = request.args.get('error')
    claims = None
    id_token = request.cookies.get("token")
    error_message = None

    if id_token:
        try:

            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            error_message = str(exc)

    return render_template('driver.html', teamNames=teamNames, user=claims, drivers=drivers, error=error)


@app.route('/compare_drivers')
def compare_drivers():

    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    drivers = list(Driver.retrieve_drivers())

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            return render_template('compareDrivers.html', user=claims, drivers=drivers)

        except ValueError as exc:
            error_message = str(exc)
    return redirect(url_for('root'))


@app.route('/compare_teams')
def compare_teams():
    teamNames = list(Team.retrieve_teams())

    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            return render_template('compareTeams.html', user=claims, teamNames=teamNames)

        except ValueError as exc:
            error_message = str(exc)

    return redirect(url_for('root'))


@app.route('/compare_t', methods=['POST'])
def Compare_T():
    team1_name = request.form['team1']
    team2_name = request.form['team2']
# we search for each team separately and pass the result to our render
    team1 = datastore_client.get(
        datastore_client.key('Teams', team1_name))
    team2 = datastore_client.get(
        datastore_client.key('Teams', team2_name))

    teamNames = list(Team.retrieve_teams())
    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)
    return render_template('/compareTeams.html', user=claims, team1=team1, team2=team2, teamNames=teamNames)


@app.route('/compare', methods=['POST'])
def Compare():
    driver1_name = request.form['driver1']
    driver2_name = request.form['driver2']
    driver1 = datastore_client.get(
        datastore_client.key('Drivers', driver1_name))
    driver2 = datastore_client.get(
        datastore_client.key('Drivers', driver2_name))

    drivers = list(Driver.retrieve_drivers())

    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)
    return render_template('/compareDrivers.html', user=claims, driver1=driver1, driver2=driver2, drivers=drivers)


@app.route('/add_driver', methods=['POST'])
def addDriver():

    error = None
    id_token = request.cookies.get("token")
    claims = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            name = request.form['firstName']
            age = int(request.form['age'])
            pole_positions = int(request.form['pole_positions'])
            total_race_wins = int(request.form['total_race_wins'])
            total_points_scored = int(request.form['total_points_scored'])
            total_world_titles = int(request.form['total_world_titles'])
            total_fastest_laps = int(request.form['total_fastest_laps'])
            team_name = request.form['team']

            try:
                Driver.create_driver(name, age,
                                     pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name)
            except ValueError as exc:
                error = str(exc)
            return redirect(url_for('drivers', error=error))

        except ValueError:
            return redirect(url_for('/'))


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

    return render_template('index.html', user=claims, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
