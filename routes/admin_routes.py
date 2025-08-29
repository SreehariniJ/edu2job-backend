from flask import Blueprint, jsonify
from utils.auth import role_required

admin_routes = Blueprint("admin_routes", __name__)

# Example: Admin dashboard
@admin_routes.route("/dashboard", methods=["GET"])
@role_required("admin")
def dashboard():
    return jsonify({"message": "Welcome Admin! This is your dashboard."}), 200

# Example: Manage users
@admin_routes.route("/users", methods=["GET"])
@role_required("admin")
def list_users():
    from models.user import User
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role}
        for u in users
    ]), 200
