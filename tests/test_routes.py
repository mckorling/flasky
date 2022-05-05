# we aren't importing anything!
# pytest will load in conftest.py and fixtures will be set up
# we can just start writing tests, easy


from app.models.cats import Cat


def test_get_all_cats_with_empty_db_returbs_empty_list(client):
# pytest sees client passed in and will go to the fixtures, set it up, and pass it in
    response = client.get("/cats")
    response_body = response.get_json()
    # this will have the status code

    # the request should work, but just return an []
    assert response.status_code == 200
    assert response_body == []

# need the client and new fixture that has the cat data
def test_get_one_cat_with_populated_db_returns_cat_json(client, seven_cats):
    response = client.get("/cats/1")
    response_body = response.get_json()

    assert response.status_code == 200
    # id=1, name="Jazz", color="black", age=8
    assert response_body == {
        "id": 1,
        "name": "Jazz",
        "color": "black",
        "age": 8
    } 

def test_get_all_cats_with_populated_db_returns_populated_list(client, seven_cats):
    response = client.get("/cats")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 7
    # can add more asserts later to check each cat is correct

def test_post_one_cat_creates_cat_in_db(client):
    # won't pass in any fixture with cat data
    # it's simpler if the database starts empty to test something added to it
    # client is like postman, and is constructed in conftest
    # we can send requests to our app and get response back by going through test client
    response = client.post("/cats", json={
        "name": "Bernie", "age": 14, "color": "grey"})
        # don't need "id" key, we want the database to use autopopulate via the route
        # if we look at the post method in cats.py, no id is passed in to Cat instantiation
    response_body = response.get_json()

    assert response.status_code == 201
    assert "id" in response_body
    assert "message" in response_body
    # won't assert the value of either, because they both use cat_id
    # most likely the id is 1 because it's the first entry
    # but we can't be sure, so we won't test it
    # this is a workaround and we are looking into the database now using query.all()
    cats = Cat.query.all()
    assert len(cats) == 1
    assert cats[0].name == "Bernie"
    assert cats[0].age == 14
    assert cats[0].color == "grey"

# we also want to test the failure behavior
def test_get_one_cat_with_empty_db_returns_404(client):
    response = client.get("/cats/1")
    assert response.status_code == 404