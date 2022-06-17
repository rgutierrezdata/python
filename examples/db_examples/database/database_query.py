import sqlalchemy as database

# Connection settings
db_string  = 'postgresql://postgres:01071998@localhost:5432/dr3db_v2'
db         = database.create_engine(db_string)
meta       = database.MetaData(db)
connection = db.connect()

# Db tables
logger_table = database.Table('logger',     meta, autoload = True, autoload_with = db)
events_table = database.Table('event_type', meta, autoload = True, autoload_with = db)

# def insert_data(fname, lname, pet):
#   a= db.execute("INSERT INTO students (fname, lname, pet) VALUES ('Roberto', 'Gutiérrez', 'Owl');") 
#   return a