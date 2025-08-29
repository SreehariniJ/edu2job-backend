from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from models.education import Education
from models.user import User

education_routes = Blueprint("education_routes", __name__)

@education_routes.route("/", methods=["POST"])
@jwt_required()
def add_education():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    data = request.json
    degree = data.get("degree")
    institution = data.get("institution")
    year = data.get("year")

    if not degree or not institution or not year:
        return jsonify({"error": "All fields required"}), 400

    edu = Education(degree=degree, institution=institution, year=year, user=user)
    db.session.add(edu)
    db.session.commit()

    return jsonify({"message": "Education added"}), 201


@education_routes.route("/", methods=["GET"])
@jwt_required()
def get_educations():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    return jsonify([
        {"id": e.id, "degree": e.degree, "institution": e.institution, "year": e.year}
        for e in user.educations
    ]), 200


@education_routes.route("/<int:edu_id>", methods=["PUT"])
@jwt_required()
def update_education(edu_id):
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    edu = Education.query.filter_by(id=edu_id, user_id=user.id).first()
    if not edu:
        return jsonify({"error": "Education not found"}), 404

    data = request.json
    edu.degree = data.get("degree", edu.degree)
    edu.institution = data.get("institution", edu.institution)
    edu.year = data.get("year", edu.year)
    db.session.commit()

    return jsonify({"message": "Education updated"}), 200


@education_routes.route("/<int:edu_id>", methods=["DELETE"])
@jwt_required()
def delete_education(edu_id):
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    edu = Education.query.filter_by(id=edu_id, user_id=user.id).first()
    if not edu:
        return jsonify({"error": "Education not found"}), 404

    db.session.delete(edu)
    db.session.commit()
    return jsonify({"message": "Education deleted"}), 200
