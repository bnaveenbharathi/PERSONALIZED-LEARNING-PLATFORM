from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['feedback']
collection = db['form']

@app.route('/')
def index():
    return render_template('feedback.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert the feedback into MongoDB
        feedback_data = {
            'name': name,
            'email': email,
            'message': message
        }
        collection.insert_one(feedback_data)

        # After submission, render the thank you page
        return render_template('thankyou.html')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
