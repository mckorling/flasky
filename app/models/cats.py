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

    # connect one - many relationship
    # add foreign key (this is the many side)
    human_id = db.Column(db.Integer, db.ForeignKey('human.id'))
    
    # create an attr that can hold a list of human(s)
    # tie the Cat to a Human record
    # "Human" -> this is the table to which Cat has a relationship
    # back_populates -> returns a list of object(s) to what table it's tied to (?)
        # it needs the attribute in the parent (same in child) model
        # in this case it is the parent model, we will make the attribute 'cats' in Human
    human = db.relationship("Human", back_populates="cats")