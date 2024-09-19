"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyCSjMOfwL6A5HMA-fUt8-zaO6M-1LKD-ZM")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,

)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Generate A Course Tutorial on Following Detail With field as Course Name, Description, Along with Chapter Name, about, Duration: Category: 'Programming', Topic: Python, Level:Basic, Duration: 1 hours, NoOf Chapters:5, in JSON format\n24 Θ\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Course Name\": \"Introduction to Python\",\n  \"Description\": \"A beginner-friendly course to learn the fundamentals of Python programming.\",\n  \"Category\": \"Programming\",\n  \"Topic\": \"Python\",\n  \"Level\": \"Basic\",\n  \"Duration\": \"1 hour\",\n  \"NoOfChapters\": 5,\n  \"Chapters\": [\n    {\n      \"Chapter Name\": \"Welcome to Python\",\n      \"About\": \"Introduction to Python, its uses, and setting up your programming environment.\",\n      \"Duration\": \"10 minutes\" \n    },\n    {\n      \"Chapter Name\": \"Variables and Data Types\",\n      \"About\": \"Learn about different data types in Python like numbers, strings, and booleans, and how to work with variables.\",\n      \"Duration\": \"15 minutes\"\n    },\n    {\n      \"Chapter Name\": \"Operators and Expressions\",\n      \"About\": \"Explore various operators in Python for performing arithmetic, comparison, and logical operations.\",\n      \"Duration\": \"15 minutes\"\n    },\n    {\n      \"Chapter Name\": \"Control Flow\",\n      \"About\": \"Understand how to control the flow of your program using conditional statements (if-else) and loops.\",\n      \"Duration\": \"15 minutes\"\n    },\n    {\n      \"Chapter Name\": \"Functions\",\n      \"About\": \"Learn to write reusable blocks of code called functions to perform specific tasks.\",\n      \"Duration\": \"5 minutes\"\n    }\n  ]\n}\n``` \n",
      ],
    },
  ]
)

response = chat_session.send_message(
"""Generate A Course Tutorial on Following Detail With field as Course Name, Description, Along with Chapter Name, about, Duration with each topic have the 10 questions with 5 options:""")
print(response.text)