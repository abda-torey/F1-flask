from google.cloud import datastore

datastore_client = datastore.Client()

class Driver:
    # function for pushing driver details to the datastore   
    def create_driver(name, age, pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name):
        # setting name as the key to prevent duplicate names
        entity_key = datastore_client.key('Drivers', name)

        query = datastore_client.query(kind='Drivers')
        # check if name already exists,if not add new driver
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

    # function for updating driver details in the datastore
    def update_driver(name, age, pole_positions, total_race_wins, total_points_scored, total_world_titles, total_fastest_laps, team_name):
        entity_key = datastore_client.key('Drivers', name)
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
    # deleting driver entity from datastore
    def delete_driver(name):
        entity_key = datastore_client.key('Drivers', name)
        datastore_client.delete(entity_key)



    # retrieve all drivers
    def retrieve_drivers():
        query = datastore_client.query(kind='Drivers')
        drivers = query.fetch()

        return drivers