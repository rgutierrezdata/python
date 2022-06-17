from flask import Blueprint, jsonify, request
from .http_requests import *

http_requests_handlers = Blueprint('http_requests_handlers', __name__, url_prefix = '/api/v1/http_requests')

#GET
@http_requests_handlers.get('/')
def get_http_requests():
  return jsonify({'route': 'http_requests'})

#POST
@http_requests_handlers.post('/post_data')
def post_example(fname, lname, pet):
  fname = request.json['fname']
  lname = request.json['lname']
  pet = request.json['pet']

  data = insert_data(fname, lname, pet)
  print("Result from insert ===>", data)
  return {"student": "a student"}