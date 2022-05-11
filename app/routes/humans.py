
import re
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.humans import Human
from app.models.cats import Cat
from app import db

humans_bp = Blueprint("humans_bp", __name__, url_prefix="/humans")

@humans_bp.route("", methods=["POST"])
def create_one_human():
    request_body = request.get_json()

    new_human = Human(name=request_body["name"]) # don't need to specify id

    db.session.add(new_human)
    db.session.commit()
    
    return {"message": f"Successfully created {new_human.name}"}, 201

@humans_bp.route("", methods=["GET"])
def get_all_humans():
    humans = Human.query.all()

    response = []

    for human in humans:
        response.append({
            "name": human.name,
            "id": human.id
        })
    
    return jsonify(response), 200


def validate_human(human_id):
    try:
        human_id = int(human_id)
    except:
        abort(make_response({"message": f"Invalid id: {human_id}"}, 400))

    # human object
    human = Human.query.get(human_id)

    if not human:
        abort(make_response({"message": f"No human with id {human_id}"}, 404))
    
    return human

# create new cat and know who the owner is
@humans_bp.route("/<human_id>/cats", methods=["POST"])
def create_cat(human_id):
    human = validate_human(human_id)

    request_body = request.get_json()

    new_cat = Cat(
        name=request_body["name"],
        age=request_body["age"],
        color=request_body["color"],
        # instead of passing in human_id, can pass in a Human object
        # don't need to add a foreign key at all
        human=human
    )

    db.session.add(new_cat)
    db.session.commit()

    return {"message": f"Cat {new_cat.name} successfully created for {human.name}"}, 201

@humans_bp.route("/<human_id>/cats", methods=["GET"])
def get_cats_by_human(human_id):
    human = validate_human(human_id)

    # instead of this, can we do Cat.query.filter or filter_by (human_id) ???
    # but then we still need to format it with same for loop below, so it's more work than needed
    response = []

    # flask sqlalchemy has established a relationship between human-cat
    for cat in human.cats:
        response.append({
            "id": cat.id,
            "name": cat.name,
            "age": cat.age,
            "color": cat.color
        })
    return jsonify(response), 200

# Right now code doesn't handle duplicates? There is a way to do so in sqlalchemy/flask (?)