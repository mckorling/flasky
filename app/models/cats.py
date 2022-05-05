# models come from sqlalchemy, now we can use that sqlalchemy object
from app import db

# model is a class that can talk to a database
# Cat inherits from the Model class in sqlalchemy
class Cat(db.Model):
    # create class variables, not instance variables
    # treat each variable/attr as a column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    color = db.Column(db.String)
    # here we don't need to use the same datatypes as SQL
    # the Model class just needs to know if it's a string, etc.
    # this is "sql stuff with python syntax"