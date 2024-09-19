from flask import Flask,render_template as render,redirect,request,session,url_for
from components.connection import connection
from components.auth import auth_routes
from components.bot import bot_routes
from components.info import info_routes
from components.dashboard import dashboard_routes
import os

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

# port run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8000",debug=True)