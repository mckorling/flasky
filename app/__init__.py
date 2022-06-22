from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS # front end flasky need

# to use the tools above, we need to create objects for them
# create it in global scope so that other files will be able to use it
db = SQLAlchemy()
migrate = Migrate()
load_dotenv() # this will load in the .env file into the environmental variables

def create_app(testing=None):
    # __name__ stores the name of the module we're in (placeholder)
    app = Flask(__name__)
    CORS(app) # front end flasky need

    # connect our database to app and tell it where it is
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # gets rid of some little error
    if testing is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TESTING_SQLALCHEMY_DATABASE_URI")
        
    # initialize objects so that they can work inside of our function?
    db.init_app(app) # database now knows the flask server we are working with
    migrate.init_app(app, db)

    # tell flask about our new cats model (in model/cats.py)
    # we import here to avoid circular imports becacuse db is imported at
    # the top of model/cats.py
    # the '.'models is shorthand for app.models... shorthand for the current directory
    from .models.cats import Cat
    # (now we can do flask db init in terminal (only ONCE per project))
    # then generate a migration in terminal: flask db migrate -m "type some message"
    # database changes are anytime we want to CRUD a record form our database
    # these migrations won't update the database though until we tell it
    # so, in terminal: flask db upgrade
    # can go into postgres to check, shortcut to correct database
    # psql -U postgres -d cats_development
    # \d to see table layout
    from .models.humans import Human
    # tell Flask that we have a new model, just import, Flask knows what to do
    # next migrate to database
    

    from .routes.cats import cats_bp
    app.register_blueprint(cats_bp)
    from .routes.humans import humans_bp
    app.register_blueprint(humans_bp)

    return app