from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from models.experience import Experience
from models.user import User

experience_routes = Blueprint("experience_routes", __name__)

@experience_routes.route("/", methods=["POST"])
@jwt_required()
def add_experience():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    data = request.json
    title = data.get("title")
    company = data.get("company")
    start_year = data.get("start_year")
    end_year = data.get("end_year")
    description = data.get("description")

    if not title or not company or not start_year:
        return jsonify({"error": "Title, company and start_year required"}), 400

    exp = Experience(
        title=title, company=company,
        start_year=start_year, end_year=end_year,
        description=description, user=user
    )
    db.session.add(exp)
    db.session.commit()
    return jsonify({"message": "Experience added"}), 201


@experience_routes.route("/", methods=["GET"])
@jwt_required()
def get_experiences():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    return jsonify([
        {
            "id": e.id, "title": e.title, "company": e.company,
            "start_year": e.start_year, "end_year": e.end_year,
            "description": e.description
        }
        for e in user.experiences
    ]), 200


@experience_routes.route("/<int:exp_id>", methods=["PUT"])
@jwt_required()
def update_experience(exp_id):
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    exp = Experience.query.filter_by(id=exp_id, user_id=user.id).first()
    if not exp:
        return jsonify({"error": "Experience not found"}), 404

    data = request.json
    exp.title = data.get("title", exp.title)
    exp.company = data.get("company", exp.company)
    exp.start_year = data.get("start_year", exp.start_year)
    exp.end_year = data.get("end_year", exp.end_year)
    exp.description = data.get("description", exp.description)
    db.session.commit()

    return jsonify({"message": "Experience updated"}), 200


@experience_routes.route("/<int:exp_id>", methods=["DELETE"])
@jwt_required()
def delete_experience(exp_id):
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    exp = Experience.query.filter_by(id=exp_id, user_id=user.id).first()
    if not exp:
        return jsonify({"error": "Experience not found"}), 404

    db.session.delete(exp)
    db.session.commit()
    return jsonify({"message": "Experience deleted"}), 200
