
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.cats import Cat
from app import db


""" jsonify vs make_response
flask takes a tuple and turns it into a response
where tuple[0] is dicitonary and [1] is status code

make_response can have headers added to it
they can have cookies added to it
make_response takes everything and turns it into the right type, response object??

abort is like raising an exception
can pass a response object and end the run of that endpoint 
and throw the response back"""


# convention to name blueprint class name and _bp
# __name__ points to where something is????? name of module
# what does "cats_bp" do?
cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

def get_cat_or_abort(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError: 
        response =  {"msg": f"Invalid input: {cat_id}"}
        abort(make_response(jsonify(response), 400))
    
    chosen_cat = Cat.query.get(cat_id)
    
    if chosen_cat is None:
        response = {"msg": f"Could not find cat with id {cat_id}"}
        abort(make_response(jsonify(response), 404))
    return chosen_cat
    
# interact with tables and database by using routes

@cats_bp.route("", methods=["POST"])
def create_one_cat():
    # we will use request library from flask
    # lets us get the request from the user and extract the body with:
    request_body = request.get_json()
    # make new Cat object, but make sure to import!
    # pass in info from request body as keyword args 
    # json uses key value pairs
    # kwa because the id attr is automatic in Cat
    new_cat = Cat(name=request_body["name"], 
                age=request_body["age"], 
                color=request_body["color"]) 
    # add to our database and save
    db.session.add(new_cat)
    db.session.commit() # adds cat to database and creates an id (sqlalchemy)
    # last step is API to send a response to the user
    return jsonify({
        "id": new_cat.id, # we can already access the add created after the commit
        "message": f"Successfully created new cat with id: {new_cat.id}"
    }), 201
    
@cats_bp.route("", methods=["GET"])
def get_all_cats():
    params = request.args # not a function call
    # params will be a dictionary. It will get all query params, 
    # we will have to narrow down to what we are looking for
    if "color" in params and "age" in params:
        color_name = params["color"]
        age_value = params["age"]
        cats = Cat.query.filter_by(color=color_name, age=age_value)
    elif "color" in params:
        color_name = params["color"]
        cats = Cat.query.filter_by(color=color_name)
        # filter_by takes column_name=value arg
        # in Models there is a column called 'color'
    elif "age" in params:
        age_value = params["age"] # won't need to be casted to int
        cats = Cat.query.filter_by(age=age_value)
    else:
        # if there was no "color" in params, then we still want all cats
    # use sqlalchemy built in functions and they can handle a query with specs to all
        cats = Cat.query.all()
    # now with all cat records in cats, create a response
    cats_response = []
    for cat in cats:
        cats_response.append({
            "id": cat.id,
            "name": cat.name,
            "age": cat.age,
            "color": cat.color
        })
    return jsonify(cats_response)

# api.4
@cats_bp.route("/<cat_id>", methods=["GET"])
def get_one_cat(cat_id):
    # first, consider data type
    # the parameter coming in is a string (from route needs to match def parameter)
    try:
        cat_id = int(cat_id)
    except ValueError: # ValueError can be seen in terminal, once a get request is made
        return {"msg": f"Invalid input: {cat_id}"}, 400
    # try not to use methods like isdigit, because it would still accept sup/superscripts
    # try/except is a lot more explicit
    chosen_cat = Cat.query.get(cat_id)
    
    if chosen_cat is None:
        return {"msg": f"Could not find cat with id {cat_id}"}, 404
    rsp = {
        "id": chosen_cat.id,
        "name": chosen_cat.name,
        "age": chosen_cat.age,
        "color": chosen_cat.color
    }
    return jsonify(rsp), 200

@cats_bp.route("/<cat_id>", methods=["PUT"])
def put_one_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError: 
        return {"msg": f"Invalid input: {cat_id}"}, 400
    chosen_cat = Cat.query.get(cat_id)
    if chosen_cat is None:
        return {"msg": f"Could not find cat with id {cat_id}"}, 404

    request_body = request.get_json()
    # We need to make sure that all the input from user is added
    try:
        chosen_cat.name = request_body["name"]
        chosen_cat.age = request_body["age"]
        chosen_cat.color = request_body["color"]
    except KeyError:
        return jsonify({"msg": "name, age, and color are required"}), 400
    # this commit will still only happen if try block executes successfully
    db.session.commit()

    return jsonify({"message": f"{cat_id} successfully updated"}), 200

@cats_bp.route("/<cat_id>", methods=["DELETE"])
def delete_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError: 
        return {"msg": f"Invalid input: {cat_id}"}, 400
    chosen_cat = Cat.query.get(cat_id)
    if chosen_cat is None:
        return {"msg": f"Could not find cat with id {cat_id}"}, 404
        
    db.session.delete(chosen_cat)
    db.session.commit()

    return {"msg": "Cat successfully deleted"}

# Adding query params







#------------------------Will refactor routes with api.3 lesson-----------------------------------------------------------
# moving to /models/cats.py
# class Cat:
#     def __init__(self, id, name, age, color):
#         self.id = id
#         self.name = name
#         self.age = age
#         self.color = color

# will be hard coding data now, so we won't need this (api.3)
# cat_1 = Cat(1, "Chidi", 4, "black")
# cat_2 = Cat(2, "Simba", 8, "orange")
# cat_3 = Cat(3, "Tucker", 2, "brown")
# cats = [cat_1, cat_2, cat_3]



# for routes, the function name can be 'anything'
# @cats_bp.route("", methods=["GET"]) 
# # "" = inherites the url_prefix from cats_bp
# # will only response to "GET"
# def get_all_cats():
#     # endpoint created
#     cat_response = []
#     # can't send back cats list because data needs to be in JSON, convert it to {}
#     for cat in cats:
#         cat_response.append({
#             'id': cat.id,
#             'name': cat.name,
#             'age': cat.age,
#             'color': cat.color
#         })
#     return jsonify(cat_response) # can specify return code
#     # need to jsonify this because it is a list of cats
#     # if it were just a dictionary, that is similar enough to json that it doesn't need it


# # there is some type of converter code that can be added like: "/<int: cat_id>"
# # however that is less flexible when handling errors, it's less customizable 
# # what is below is a more flexible
# @cats_bp.route("/<cat_id>", methods=["GET"])
# def get_one_cat(cat_id):
#     # first, consider data type
#     # the parameter coming in is a string (from route needs to match def parameter)
#     try:
#         cat_id = int(cat_id)
#     except ValueError: # ValueError can be seen in terminal, once a get request is made
#         return {"msg": f"Invalid input: {cat_id}"}, 400
#     # try not to use methods like isdigit, because it would still accept sup/superscripts
#     # try/except is a lot more explicit
#     chosen_cat = None
#     for cat in cats:
#         if cat.id == cat_id:
#             chosen_cat = cat
#             break # consider time complexity, no need to continue loop once found
#     # cat hasn't been found
#     if chosen_cat is None:
#         return {"msg": f"Could not find cat with id {cat_id}"}, 404
    
#     # cat has been found!
#     # but can't just return a cat object, because http won't understand that
#     # needs to be in json (aka python dict), flask auto converts python dict to json
#     response = {
#             'id': chosen_cat.id,
#             'name': chosen_cat.name,
#             'age': chosen_cat.age,
#             'color': chosen_cat.color
#     }
#     return response, 200
#     # companies will have their own pattern for how they want responses formated
#     # for example using "msg" or "message", etc.
#     # flask decides the error codes
