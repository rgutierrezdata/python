import sqlalchemy as database
import os

db_string = os.environ.get("CONNECTION_STRING")
db = database.create_engine(db_string)
connection = db.connect()

Result = connection.execute("SELECT * FROM students")
ResultSet = Result.fetchall()

print("valores", ResultSet)


#app.config['SQLALCHEMY_DATABASE_URI']='postgres:masterkey@localhost/students'
#db = SQLAlchemy(app)


def insert_data(fname, lname, pet):
    a = db.execute("INSERT INTO students (fname, lname, pet) VALUES ('Roberto', 'Gutiérrez', 'Owl');") 
    return a 