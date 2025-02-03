from pony.orm import *

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Optional(str, unique=True)

    cars = Set("Car")


class Car(db.Entity):
    id = PrimaryKey(int, auto=True)
    model = Required(str)
    year = Optional(int)
    user = Required(User)
