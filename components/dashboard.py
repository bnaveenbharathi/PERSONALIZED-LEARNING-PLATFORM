from flask import Blueprint, jsonify, session
from .connection import connection
import logging
import traceback
from bson import ObjectId

dashboard_routes = Blueprint('dashboard', __name__)

# DB connection
db = connection()
userinfomain = db["info"]
users = db["users"]

logging.basicConfig(level=logging.DEBUG)

def serialize_document(doc):
    if doc is not None:
        doc['_id'] = str(doc['_id'])
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, dict):
                doc[key] = serialize_document(value)
            elif isinstance(value, list):
                doc[key] = [serialize_document(item) if isinstance(item, dict) else item for item in value]
    return doc

@dashboard_routes.route("/student-profile", methods=["GET"])
def student_profile():
    try:
        if 'logged_in' not in session or not session['logged_in']:
            logging.debug("User not logged in")
            return jsonify({"error": "User not logged in"}), 401

        email = session.get('email')
        logging.debug(f"Looking up user with email: {email}")
        user = users.find_one({"email": email})

        if not user:
            logging.debug(f"User not found for email: {email}")
            return jsonify({"error": "User not found"}), 404

        user_id = user.get('_id')

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        user_data_cursor = userinfomain.find({"user_id": user_id})
        user_data_list = list(user_data_cursor)

        if not user_data_list:
            logging.debug(f"User profile not found for user ID: {user_id}")
            return jsonify({"error": "User profile not found"}), 404
        
        user_data = serialize_document(user_data_list[0])
        user_data['user'] = serialize_document(user)

        # logging.debug(f"User profile data: {user_data}")

        return jsonify(user_data), 200

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}", "trace": traceback.format_exc()}), 500
