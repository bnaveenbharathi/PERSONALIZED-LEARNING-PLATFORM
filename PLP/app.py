from flask import Flask,render_template as render,redirect,request,session,url_for
from components.connection import connection
from components.auth import auth_routes

app=Flask(__name__)
app.config["SECRET_KEY"]='123890'


# authentication
app.register_blueprint(auth_routes,url_prefix="/auth")

#routes
@app.route("/")
def authentication():
    return render("user.html")

@app.route("/home")
def home():
    if 'logged_in' in session and session['logged_in']:
        return render('index.html')
    else:
        return redirect(url_for("authentication"))

# port run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8000",debug=True)