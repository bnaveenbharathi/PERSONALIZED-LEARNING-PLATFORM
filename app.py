from flask import Flask,render_template as render,redirect,request,session,url_for,jsonify
from components.connection import connection
from components.auth import auth_routes
from components.bot import bot_routes
from components.info import info_routes
from components.dashboard import dashboard_routes
import os
import google.generativeai as genai
import requests
import isodate 

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
    
@app.route("/student-progress")
def studentdashboardprogress():
    if 'logged_in' in session and session['logged_in']:
        return render('dashboard-progress.html',title=title)
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
youtube_api_key = "AIzaSyBQ5PCuvFyeNCq5hWaN6BeK4KMg5NkKY1M"
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
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={title}&relevanceLanguage=en&type=video&key={youtube_api_key}"
    response = requests.get(search_url)
    data = response.json()
    
    print("API Response:", data)  

    try:
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            video_id = item['id'].get('videoId', None)
            if video_id:
                # Get video details including duration
                video_details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={youtube_api_key}"
                details_response = requests.get(video_details_url)
                video_details = details_response.json()
                
                if 'items' in video_details and len(video_details['items']) > 0:
                    # Get the video duration in ISO 8601 format and convert to minutes
                    duration_iso = video_details['items'][0]['contentDetails']['duration']
                    duration = isodate.parse_duration(duration_iso)
                    duration_in_minutes = int(duration.total_seconds() // 60)
                    
                    # Customize the YouTube embed URL to hide controls, branding, etc.
                    video_url = (f"https://www.youtube.com/embed/{video_id}"
                                 f"?controls=0&modestbranding=1&rel=0&showinfo=0&autohide=1")
                    return video_url, item['snippet']['title'], f"{duration_in_minutes} minutes"
    except KeyError as e:
        print(f"KeyError: {e} - The key was not found in the API response.")
    
    return None, None, None
@app.route('/courses')
def course():
    return render('courserecommendation.html',title=title)


@app.route('/generate_course', methods=['POST'])
def generate_course():
    category = request.form['category']
    topic = request.form['topic']
    level = request.form['level']
    duration = request.form['duration']
    no_of_chapters = int(request.form['no_of_chapters'])

   
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



if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8000",debug=True)