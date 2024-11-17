from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import error_response,validate_fields
from datetime import datetime
from app.models import hash_password

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/create", methods=["POST"])
def create_admin():
    data = request.json
    valid, error = validate_fields(data, ["username", "password", "email"])
    if not valid:
        return error_response(error, 400)

    db = current_app.db
    if db.users.find_one({"username": data["username"]}):
        return jsonify({"error": "Admin username already exists"}), 400

    hashed_password = hash_password(data["password"])
    db.users.insert_one({
        "username": data["username"],
        "password": hashed_password,
        "email": data["email"],
        "role": "admin",
        "created_at": datetime.now()
    })
    return jsonify({"message": "Admin created successfully"}), 201


@admin_bp.route("/login", methods=["POST"])
def login_admin():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    db = current_app.db
    admin = db.users.find_one({"username": data["username"], "role": "admin"})
    if not admin or not verify_password(data["password"], admin["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token for admin
    access_token = create_access_token(identity={"username": admin["username"], "role": admin["role"]})
    return jsonify({"token": access_token}), 200

@admin_bp.route("/assignments", methods=["GET"])
@jwt_required()
def view_assignments():
    current_user = get_jwt_identity()
    db = current_app.db
    assignments = db.assignments.find({"admin": current_user["username"], "status": "pending"})
    return jsonify([{
        "user": assignment["user"],
        "task": assignment["task"],
        "timestamp": assignment["timestamp"]
    } for assignment in assignments]), 200

@admin_bp.route("/assignments/<assignment_id>/accept", methods=["POST"])
@jwt_required()
def accept_assignment(assignment_id):
    db = current_app.db
    assignment = db.assignments.find_one({"_id": assignment_id, "status": "pending"})
    if not assignment:
        return jsonify({"error": "Assignment not found or already processed"}), 404

    db.assignments.update_one({"_id": assignment_id}, {"$set": {"status": "accepted", "processed_at": datetime.now()}})
    return jsonify({"message": "Assignment accepted"}), 200

@admin_bp.route("/assignments/<assignment_id>/reject", methods=["POST"])
@jwt_required()
def reject_assignment(assignment_id):
    db = current_app.db
    assignment = db.assignments.find_one({"_id": assignment_id, "status": "pending"})
    if not assignment:
        return jsonify({"error": "Assignment not found or already processed"}), 404

    db.assignments.update_one({"_id": assignment_id}, {"$set": {"status": "rejected", "processed_at": datetime.now()}})
    return jsonify({"message": "Assignment rejected"}), 200
