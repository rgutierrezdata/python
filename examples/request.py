from flask import Blueprint, jsonify
import requests

request = Blueprint("request",__name__, url_prefix="/api/v1/request")

@request.get("/pokemon")
def requestFunc():
    res = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
    return res.json()
