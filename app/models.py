from pony.orm import *

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Optional(str, unique=True)
    name = Required(str)

    cars = Set("Car")


class Car(db.Entity):
    id = PrimaryKey(int, auto=True)
    model = Required(str)
    year = Optional(int)
    user = Required(User)

# Connect to your database (replace with your connection string)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)