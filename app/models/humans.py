from app import db

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    # connect to Child class (Cat)
    # first arg is the Table to connect to
    # back_populates connects it to a specfic attribute to return in Human
    cats = db.relationship("Cat", back_populates="human")