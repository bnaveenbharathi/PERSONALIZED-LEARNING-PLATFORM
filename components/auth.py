from flask import Flask, jsonify, request, session, redirect, url_for,Blueprint
from werkzeug.security import generate_password_hash as gen, check_password_hash as check
from .connection import connection

auth_routes = Blueprint('auth', __name__)

# DB connection
db = connection()
users = db["users"]

# Registration route
@auth_routes.route("/register", methods=['POST'])
def register():
    data = request.json
    name = data.get("name")
    age = data.get('age')
    email = data.get('email')
    password = data.get('password')
    hash_pass = gen(password)
    existing_user = users.find_one({"email": email})
    
    if existing_user:
        return jsonify({"existsmessage": "User already exists"}), 400
    
    new_user = {
        'name': name,
        'age': age,
        'email': email,
        'pass': hash_pass
    }
    users.insert_one(new_user)
    return jsonify({"message": "User registered successfully"}), 201

# Login route
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    existing_user = users.find_one({"email": email})
    
    if existing_user and check(existing_user['pass'], password):
        session['email'] = email
        session['logged_in'] = True
        return jsonify({'message': "Login Successful"}), 200
    return jsonify({"invalidmessage": "Invalid email or password"}), 401

# Logout route
@auth_routes.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for("authentication"))
