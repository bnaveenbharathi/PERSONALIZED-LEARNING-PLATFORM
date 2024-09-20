from flask import Flask, render_template, request

app = Flask(__name__)

# Sample MCQ data (10 questions)
mcqs = [
    {
        "QUESTION": "What is the primary purpose of test analysis in software testing?",
        "OPTIONS": {
            "A": "To identify and prioritize test conditions.",
            "B": "To execute test cases and report defects.",
            "C": "To design and document test cases.",
            "D": "To track and monitor the progress of testing."
        },
        "ANSWER": "A"
    },
    {
        "QUESTION": "Which of the following is not a valid HTTP method?",
        "OPTIONS": {
            "A": "GET",
            "B": "POST",
            "C": "PULL",
            "D": "DELETE"
        },
        "ANSWER": "C"
    },
    {
        "QUESTION": "Which keyword is used to define a function in Python?",
        "OPTIONS": {
            "A": "def",
            "B": "function",
            "C": "fun",
            "D": "define"
        },
        "ANSWER": "A"
    },
    {
        "QUESTION": "What is the correct file extension for Python files?",
        "OPTIONS": {
            "A": ".pyt",
            "B": ".py",
            "C": ".pt",
            "D": ".p"
        },
        "ANSWER": "B"
    },
    {
        "QUESTION": "Which of these is not a Python core data type?",
        "OPTIONS": {
            "A": "List",
            "B": "Dictionary",
            "C": "Tuples",
            "D": "Class"
        },
        "ANSWER": "D"
    },
    {
        "QUESTION": "What does CSS stand for?",
        "OPTIONS": {
            "A": "Creative Style Sheets",
            "B": "Cascading Style Sheets",
            "C": "Computer Style Sheets",
            "D": "Colorful Style Sheets"
        },
        "ANSWER": "B"
    },
    {
        "QUESTION": "What is the default HTTP port number?",
        "OPTIONS": {
            "A": "21",
            "B": "80",
            "C": "8080",
            "D": "443"
        },
        "ANSWER": "B"
    },
    {
        "QUESTION": "Which of these is a backend programming language?",
        "OPTIONS": {
            "A": "HTML",
            "B": "CSS",
            "C": "JavaScript",
            "D": "Python"
        },
        "ANSWER": "D"
    },
    {
        "QUESTION": "Which method is used to remove whitespace from both ends of a string in Python?",
        "OPTIONS": {
            "A": "strip()",
            "B": "trim()",
            "C": "len()",
            "D": "split()"
        },  
        "ANSWER": "A"
    },
    {
        "QUESTION": "In which year was Python first released?",
        "OPTIONS": {
            "A": "1989",
            "B": "1991",
            "C": "2000",
            "D": "1995"
        },
        "ANSWER": "B"
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_answers = request.form
        score = 0
        
        # Check user's answers and calculate score
        for i, mcq in enumerate(mcqs):
            if mcq['ANSWER'] == user_answers.get(f"answer-{i}"):
                score += 1
        
        return render_template("result.html", score=score, total=len(mcqs))
    
    return render_template("index.html", mcqs=mcqs)

if __name__ == "__main__":
    app.run(debug=True) 