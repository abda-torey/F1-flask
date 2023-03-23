from google.cloud import datastore

datastore_client = datastore.Client()


class Team:

    # this function pushes team details to the datastore
    def create_team(name, year_founded, total_p_pos, total_race_w, total_c_titles, prevSeason_pos):
        entity_key = datastore_client.key('Teams', name)
        query = datastore_client.query(kind='Teams')
         # check if name already exists,if not add new team
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

    # function for updating team details

    def update_team_details(name, year_founded, total_p_pos, total_race_w, total_c_titles, prevSeason_pos):
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
    # function for deleting an a team entity from the datastore

    def delete_team(name):
        entity_key = datastore_client.key('Teams', name)
        datastore_client.delete(entity_key)
# retrieving all teams details

    def retrieve_teams():
        query = datastore_client.query(kind='Teams')
        teams = query.fetch()

        return teams
