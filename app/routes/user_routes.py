from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from app.models import hash_password, verify_password
from app.utils import error_response, validate_fields
from datetime import datetime

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.json
    valid, error = validate_fields(data, ["username", "password", "email"])
    if not valid:
        return error_response(error, 400)

    db = current_app.db
    if db.users.find_one({"username": data["username"]}):
        return jsonify({"error": "Username already exists"}), 400
    
    hashed_password = hash_password(data["password"])
    db.users.insert_one({
        "username": data["username"],
        "password": hashed_password,
        "email": data["email"],
        "role": "user",
        "created_at": datetime.now()
    })
    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    db = current_app.db
    user = db.users.find_one({"username": data["username"]})
    if not user or not verify_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity={"username": user["username"], "role": user["role"]})
    return jsonify({"token": access_token}), 200


@user_bp.route("/upload", methods=["POST"])
def upload_assignment():
    data = request.json
    if not data:
        return error_response("Invalid input: No data provided", 400)

    # Check for required fields
    valid, error = validate_fields(data, ["task", "admin", "userId"])
    if not valid:
        return error_response(error, 400)

    db = current_app.db
    admin = db.users.find_one({"username": data["admin"], "role": "admin"})
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    db.assignments.insert_one({
        "user": data.get("userId"),
        "task": data.get("task"),
        "admin": data.get("admin"),
        "status": "pending",
        "timestamp": datetime.now()
    })
    return jsonify({"message": "Assignment uploaded successfully"}), 201

@user_bp.route("/admins", methods=["GET"])
def get_all_admins():
    db = current_app.db
    admins = db.users.find({"role": "admin"}, {"_id": 0, "username": 1})
    return jsonify(list(admins)), 200

@user_bp.route("/test_db_connection", methods=["GET"])
def test_db_connection():
    try:
        # Test if the MongoDB connection is working by checking if the database exists
        db = current_app.db
        # List all collections in the database (can be changed to any other query you like)
        collections = db.list_collection_names()
        
        if collections:
            return jsonify({"message": "MongoDB connected successfully", "collections": collections}), 200
        else:
            return jsonify({"error": "MongoDB connected, but no collections found"}), 400
    except Exception as e:
        return jsonify({"error": f"Error connecting to MongoDB: {str(e)}"}), 500
