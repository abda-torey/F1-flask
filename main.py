from flask import Flask, render_template, request, redirect, url_for
import google.oauth2.id_token
from google.auth.transport import requests
from google.cloud import datastore


app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()


def create_team(name, year_founded, total_p_pos, total_race_w, total_c_titles, prevSeason_pos):
    entity_key = datastore_client.key('Teams', name)
    query = datastore_client.query(kind='Teams')

    query.add_filter('name', '=', name)
    result = list(query.fetch())

    if len(result) > 0:
        raise ValueError('Team with name {} already exists.'.format(name))
    else:

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


def updateTeamDetails(name, year_founded, total_p_pos, total_race_w, total_c_titles, prevSeason_pos):
    entity_key = datastore_client.key('Teams', name)
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


def deleteTeam(name):
    entity_key = datastore_client.key('Teams', name)
    datastore_client.delete(entity_key)


def deleteDriver(name):
    entity_key = datastore_client.key('Drivers', name)
    datastore_client.delete(entity_key)


def retrieveTeams():
    query = datastore_client.query(kind='Teams')
    teams = query.fetch()

    return teams


def retrieveDrivers():
    query = datastore_client.query(kind='Drivers')
    drivers = query.fetch()

    return drivers


def create_driver(name, age, pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name):
    entity_key = datastore_client.key('Drivers', name)

    query = datastore_client.query(kind='Drivers')

    query.add_filter('name', '=', name)
    result = list(query.fetch())
    if len(result) > 0:
        raise ValueError('Driver with name {} already exists.'.format(name))
    else:
        entity = datastore.Entity(key=entity_key)

        entity.update({
            'name': name,
            'age': age,
            'pole_positions': pole_positions,
            'total_race_wins': total_race_wins,
            'total_points_scored': total_points_scored,
            'total_world_titles': total_world_titles,
            'total_fastest_laps': total_fastest_laps,
            'teamName': team_name

        })
        datastore_client.put(entity)


def updateDriver(name, age, pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps,team_name):
    entity_key = datastore_client.key('Drivers', name)
    entity = datastore.Entity(key=entity_key)

    entity.update({
        'name' : name,
        'age': age,
        'pole_positions': pole_positions,
        'total_race_wins': total_race_wins,
        'total_points_scored': total_points_scored,
        'total_world_titles': total_world_titles,
        'total_fastest_laps': total_fastest_laps,
        
        'teamName': team_name

    })
    datastore_client.put(entity)


@app.route('/filter_drivers', methods=['POST'])
def filterDriver():
    

    team = request.form['team']
    wins = request.form['wins']
    query = datastore_client.query(kind='Drivers')
    if team:
        query.add_filter('teamName', '=', team)
    if wins:
        query.add_filter('total_race_wins', '>=', wins)

    print(type(wins))
    drivers = query.fetch()

    teamNames = list(retrieveTeams())

    return render_template('driver.html', drivers=drivers, teamNames=teamNames)


@app.route('/filter_teams', methods=['POST'])
def filterTeams():
    total_c_titles = int(request.form['total_c_titles'])

    query = datastore_client.query(kind='Teams')
    if total_c_titles:
        query.add_filter('total_c_titles', '>=', total_c_titles)

    teamNames = query.fetch()

    return render_template('teams.html', teamNames=teamNames)


@app.route('/teams')
def teams():
    teamNames = retrieveTeams()
    error = request.args.get('error')

    return render_template('teams.html', teamNames=teamNames, error=error)


@app.route('/add_team', methods=['POST'])
def addTeam():

    error = None

    name = request.form['name'].lower()
    year_founded = request.form['year_founded']
    total_p_pos = int(request.form['total_p_pos'])
    total_race_w = int(request.form['total_race_w'])
    total_c_titles = int(request.form['total_c_titles'])
    prevSeason_pos = int(request.form['prevSeason_pos'])

    print(name)
    try:
        create_team(name, year_founded, total_p_pos,
                    total_race_w, total_c_titles, prevSeason_pos)
    except ValueError as exc:
        error = str(exc)

    print(error)

    return redirect(url_for('teams', error=error))
    return render_template('teams.html')


@app.route('/team_details/<string:name>')
def team_details(name):
    key = datastore_client.key('Teams', name)
    query = datastore_client.query(kind='Teams')
    query.add_filter('__key__', '=', key)
    teamDetails = query.fetch()

    return render_template('teamPage.html', teamDetails=teamDetails)


@app.route('/driver_details/<string:name>')
def driver_details(name):

    key = datastore_client.key('Drivers', name)
    query = datastore_client.query(kind='Drivers')
    query.add_filter('__key__', '=', key)
    driverDetails = query.fetch()

    return render_template('driverPage.html', driverDetails=driverDetails)


@app.route('/editable_team/<string:name>')
def editable_team(name):
    key = datastore_client.key('Teams', name)
    query = datastore_client.query(kind='Teams')
    query.add_filter('__key__', '=', key)
    teamDetails = query.fetch()

    return render_template('editTeam.html', teamDetails=teamDetails)


@app.route('/editable_driver/<string:name>')
def editable_driver(name):
    key = datastore_client.key('Drivers', name)
    query = datastore_client.query(kind='Drivers')
    query.add_filter('__key__', '=', key)
    driverDetails = query.fetch()
    teamNames = retrieveTeams()

    return render_template('editDriver.html', driverDetails=driverDetails, teamNames=teamNames)


@app.route('/update_team/<string:name>', methods=['POST'])
def update_team(name):
    name = request.form['name'].lower()
    year_founded = request.form['year_founded']
    total_p_pos = request.form['total_p_pos']
    total_race_w = request.form['total_race_w']
    total_c_titles = request.form['total_c_titles']
    prevSeason_pos = request.form['prevSeason_pos']
    updateTeamDetails(name, year_founded, total_p_pos,
                      total_race_w, total_c_titles, prevSeason_pos)

    return redirect(url_for('teams'))


@app.route('/update_driver/<string:name>', methods=['POST'])
def update_driver(name):
    teamNames = None
    team_name = None
    name = request.form['firstName'].lower()
    age = request.form['age']
    pole_positions = request.form['pole_positions']
    total_race_wins = request.form['total_race_wins']
    total_points_scored = request.form['total_points_scored']
    total_world_titles = request.form['total_world_titles']
    total_fastest_laps = request.form['total_fastest_laps']
    team_name = request.form['team']
    

    updateDriver(name, age,
                 pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name)

    return redirect(url_for('drivers'))


@app.route('/delete_team/<string:name>')
def delete_team(name):
    deleteTeam(name)

    return redirect(url_for('teams'))


@app.route('/delete_driver/<string:name>')
def delete_driver(name):
    deleteDriver(name)

    return redirect(url_for('drivers'))


@app.route('/drivers')
def drivers():
    teamNames = list(retrieveTeams())
    drivers = retrieveDrivers()
    error = request.args.get('error')

    return render_template('driver.html', teamNames=teamNames, drivers=drivers,error = error)


@app.route('/compare_drivers')
def compare_drivers():
    drivers = list(retrieveDrivers())

    return render_template('compareDrivers.html', drivers=drivers)


@app.route('/compare_teams')
def compare_teams():
    teamNames = list(retrieveTeams())

    return render_template('compareTeams.html', teamNames=teamNames)


@app.route('/compare_t', methods=['POST'])
def Compare_T():
    team1_name = request.form['team1']
    team2_name = request.form['team2']
    team1 = datastore_client.get(
        datastore_client.key('Teams', team1_name))
    team2 = datastore_client.get(
        datastore_client.key('Teams',team2_name))

    teamNames = list(retrieveTeams())
    return render_template('/compareTeams.html', team1=team1, team2=team2, teamNames=teamNames)


@app.route('/compare', methods=['POST'])
def Compare():
    driver1_name = request.form['driver1']
    driver2_name = request.form['driver2']
    driver1 = datastore_client.get(
        datastore_client.key('Drivers', driver1_name))
    driver2 = datastore_client.get(
        datastore_client.key('Drivers',driver2_name))
    
    
    drivers = list(retrieveDrivers())
    return render_template('/compareDrivers.html', driver1=driver1, driver2=driver2, drivers=drivers)


@app.route('/add_driver', methods=['POST'])
def addDriver():

    error = None
   
    name = request.form['firstName']
    age = int(request.form['age'])
    pole_positions = int(request.form['pole_positions'])
    total_race_wins = int(request.form['total_race_wins'])
    total_points_scored = int(request.form['total_points_scored'])
    total_world_titles = int(request.form['total_world_titles'])
    total_fastest_laps = int(request.form['total_fastest_laps'])
    team_name = request.form['team']
   
    try:
        create_driver(name, age,
                  pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name)
    except ValueError as exc:
        error = str(exc)



    
    return redirect(url_for('drivers', error=error))

    


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
