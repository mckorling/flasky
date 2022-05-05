# fixtures
# pytest will look for this specific file (name must always be this)
# it makes sure that the data for each test is clean and reset after each test is ran
# assuming a test modifies the data

import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cats import Cat

# for Flask, our test environment, will probably look 'exactly' like this
@pytest.fixture
def app(): # we want to test routes and the routes run inside the flask app
    app = create_app({"TESTING": True}) # pass in something that's not None, so the test environ is used

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
        # with databases, sometimes, things are commited or are waiting to be commited
        # this will remove those so that the incoming queries will look at ONLY
        # what's in the database
    
    # create our database 
    # then return the app (kinda)
    # lets us use the app
    # the yield makes it so that when we are done with it, we can do some 'cleanup'
    with app.app_context(): 
        # instantiate database, this will build all the tables (like db init, upgrade)
        db.create_all()
        # returns the app for our tests to use
        yield app # client (defined below uses the app here)
    
    # cleanup, we will start every test with a clean, fresh, empty database
    # allows us to run tests and know exactly what's in the database
    with app.app_context():
        db.drop_all()

# can't call flask run inside tests
# this fixture will set us up so that we can test with our routes with flask but w/o flask run
# will need to set up a client (kind of like Postman), Flask gives us this feature
@pytest.fixture
def client(app):
    # when app is passed in, fixture detects it
    # goes to find fixture named app (above) and constructs it for us
    # 'app' passed in must match exactly the name of the above picture (currently, ln 13)
    return app.test_client()

# Above will set up the app and client structure so that we can write tests
# We are writing an API and that is what we care about testing
#---------------------------------------------------------------------------------

# write fixtures that puts data in the database
# this way we won't have to put in data in each test

@pytest.fixture
def seven_cats(app):
    # need access to the app because the app gives us access to the database
    # name, age, color
    # typically we wouldn't add id, but for the tests we want to know exact cats and their ids
    jazz = Cat(id=1, name="Jazz", color="black", age=8)
    cosmo = Cat(id=2, name="Cosmo", color="tuxedo", age=8)
    lily = Cat(id=3, name="Lily", color="brown and black", age=6)
    ellis = Cat(id=4, name="Ellis", color="orange", age=2)
    monster= Cat(id=5, name="Monster", color="grey", age=14)
    simba = Cat(id=6, name="Simba", color="orange", age=8)
    jenkins = Cat(id=7, name="Jenkins", color="tuxedo", age=4)

    db.session.add(jazz)
    db.session.add(cosmo)
    db.session.add(lily)
    db.session.add(ellis)
    db.session.add(monster)
    db.session.add(simba)
    db.session.add(jenkins)

    # db.session_all([list of cats])

    db.session.commit()