from flask import Flask,render_template as render,redirect,request,session,url_for,jsonify
from components.connection import connection
from components.auth import auth_routes
from components.bot import bot_routes
from components.info import info_routes
from components.dashboard import dashboard_routes
import os
import google.generativeai as genai
import requests

app=Flask(__name__)
app.config["SECRET_KEY"]='123890'

title="LearnSphere"


# authentication
app.register_blueprint(auth_routes,url_prefix="/auth")
app.register_blueprint(bot_routes,url_prefix="/bot")
app.register_blueprint(info_routes,url_prefix="/info")
app.register_blueprint(dashboard_routes,url_prefix="/dashboard")

#routes
@app.route("/")
def authentication():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('home'))
    return render("user.html",title=title)

@app.route("/home")
def home():
    if 'logged_in' in session and session['logged_in']:
        return render('index.html',title=title)
    else:
        return redirect(url_for("authentication"))

@app.route("/student-dashboard")
def studentdashboard():
    if 'logged_in' in session and session['logged_in']:
        return render('student-dashboard.html',title=title)
    else:
        return redirect(url_for("authentication"))
    

@app.route("/learningbot")
def bot():
    if 'logged_in' in session and session['logged_in']:
        return render("bot.html",title=title)
    else:
        return redirect(url_for('authentication'))

@app.route("/personalinfo")
def info():
    if 'logged_in' in session and session['logged_in']:
        return render("personalinfo.html",title=title)
    else:
        return redirect(url_for('authentication'))
    

api_key = "AIzaSyBJ5ibIkwm1koegM1kCFvq3XtyO-gKFbUI"
youtube_api_key = "AIzaSyCjDu8-dniNWptu3nIamxakgs3ySDfrBPA"
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def fetch_youtube_video(title):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={title}&key={youtube_api_key}"
    response = requests.get(search_url)
    data = response.json()
    
    # Print the API response for debugging
    print("API Response:", data)    

    try:
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            video_id = item['id'].get('videoId', None)
            if video_id:
                video_url = f"https://www.youtube.com/embed/{video_id}"
                return video_url, item['snippet']['title'], '5 minutes'  # Duration is hardcoded here for simplicity
    except KeyError as e:
        print(f"KeyError: {e} - The key was not found in the API response.")
    
    return None, None, None

@app.route('/courses')
def course():
    return render('courserecommendation.html')

@app.route('/generate_course', methods=['POST'])
def generate_course():
    category = request.form['category']
    topic = request.form['topic']
    level = request.form['level']
    duration = request.form['duration']
    no_of_chapters = int(request.form['no_of_chapters'])

    # Generate course structure using AI
    chat_session = model.start_chat(
        history=[{
            "role": "user",
            "parts": [
                f"Generate a course plan in JSON format for Category: {category}, Topic: {topic}, Level: {level}, "
                f"Duration: {duration}, NoOfChapters: {no_of_chapters}."
            ],
        }]
    )
    response = chat_session.send_message("Generate the course layout.")
    course_data = response.text  # Convert the response text to appropriate JSON format (as per the Generative AI output)

    # Sample course data structure
    chapters = []
    for i in range(no_of_chapters):
        video_url, video_title, video_duration = fetch_youtube_video(f"{topic} Chapter {i + 1}")
        chapters.append({
            "title": f"{topic} Chapter {i + 1}",
            "duration": f"{30} minutes",
            "description": f"Chapter {i + 1} description for {topic}",
            "video_url": video_url,
            "video_title": video_title,
            "video_duration": video_duration,
            "code_example": "Sample code example",
            "quiz": "Sample quiz",
            "text_content": "Sample text content",
        })

    return jsonify({"chapters": chapters})


# port run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8000",debug=True)