from flask import Blueprint, jsonify, request, abort
from main import db
from models.diaries import Diary
from models.users import User
from schemas.diary_schema import diary_schema, diaries_schema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


diaries = Blueprint('diaries', __name__, url_prefix="/diaries")

# The GET routes endpoint
@diaries.route("/<int:id>/", methods=["GET"])
def get_diary(id):
    stmt = db.select(Diary).filter_by(id=id)
    card = db.session.scalar(stmt)
    #return an error if the card doesn't exist
    if not card:
        return abort(400, description= "Diary not found")
    # Convert the diaries from the database into a JSON format and store them in result
    result = diary_schema.dump(card)
    # return the data in JSON format
    return jsonify(result)