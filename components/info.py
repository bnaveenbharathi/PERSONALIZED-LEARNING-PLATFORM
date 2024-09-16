from flask import Blueprint, jsonify, request, url_for, session
from werkzeug.utils import secure_filename
from .connection import connection
import os
import traceback

info_routes = Blueprint('info', __name__)

# DB connection
db = connection()
userinfomain = db["info"]
users = db["users"]

UPLOAD_FOLDER = os.path.join('static', 'uploads/profile')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
import logging

logging.basicConfig(level=logging.DEBUG)  
@info_routes.route("/userinfo", methods=["POST"])
def userinfo():
    try:
        if 'logged_in' not in session or not session['logged_in']:
            return jsonify({"error": "User not logged in"}), 401

        email = session.get('email')
        user = users.find_one({"email": email})

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user.get('_id')

        img_url = None
        if 'profile_picture' in request.files:
            picture = request.files['profile_picture']
            if picture and picture.filename:
                filename = secure_filename(picture.filename)
                img_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    picture.save(img_path)
                    img_url = url_for('static', filename=f'uploads/profile/{filename}')
                except Exception as e:
                    return jsonify({"error": f"Failed to save profile picture: {str(e)}"}), 500

        user_data = {
            "user_id": user_id,
            "user_type": request.form.get("user_type"),
            "personal_info": request.form.get("personal_info"),
            "img_url": img_url,
            "Field_of_Study": request.form.get("Field_of_Study"),
            "study_other": request.form.get("study_other"),
            "current_job": request.form.get("current_job"),
            "experience": request.form.get("experience"),
            "job_other": request.form.get('job_other'),
            "selected_interests": request.form.get("selected_interests"),
            "interest_categories": request.form.getlist("interest_categories"),
            "skills": request.form.get("skills")
        }

        filtered_data = {key: value for key, value in user_data.items() if value and value != '' and value != []}

        result = userinfomain.insert_one(filtered_data)
        logging.debug(f"Insert Result: {result.inserted_id}")

        return jsonify({"message": "User registered successfully", "image_url": img_url}), 201

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}", "trace": traceback.format_exc()}), 500
