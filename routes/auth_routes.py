from flask import Blueprint, request, jsonify
from utils.db import db
from utils.auth import hash_password, verify_password, create_token
from models.user import User

auth_routes = Blueprint("auth_routes", __name__)

# Register
@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(user.id, user.role)
    return jsonify({"token": token, "role": user.role}), 200
