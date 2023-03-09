import google.oauth2.id_token
from flask import Flask, render_template, request, redirect
from google.auth.transport import requests


from google.cloud import datastore
client = datastore.Client()
class Team:
    def create_team(year_founded,total_p_pos,total_race_w,total_c_titles,prevSeason_pos):
        entity_key = client.entity.Key('Teams')
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'year_founded':year_founded,
            'total_p_pos':total_p_pos,
            'total_race_w':total_race_w,
            'total_c_titles':total_c_titles,
            'prevSeason_pos':prevSeason_pos
        })
        client.put(entity)
