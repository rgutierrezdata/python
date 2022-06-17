from flask import Blueprint
from .database_query import *

database = Blueprint("database", __name__, url_prefix = "/api/v1/database")

@database.get('/')
def getStudent():
	return "user created"

@database.get("/me")
def me():
  a = insert_data('fname', 'lname', 'pet')
  print("valor", a)
  return {"student": "a student"}