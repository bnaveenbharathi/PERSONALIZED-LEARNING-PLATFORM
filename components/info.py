from flask import Flask, jsonify, request, session, redirect, url_for,Blueprint
from .connection import connection

info_routes = Blueprint('info', __name__)

#DB connection
db = connection()
userinfo = db["info"]
users = db["users"]


@info_routes.route("/userinfo",methods=["POST"])
def userinfo():
    if 'logged_in' in session and session["logged_in"]:
        email=session.get("email")
        user=users.find_one({'email':email})
        if user:
            user_id=user.get("_id")
            
        