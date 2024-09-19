
import google.generativeai as genai

# Configure the API key 
api_key = "AIzaSyBJ5ibIkwm1koegM1kCFvq3XtyO-gKFbUI"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Generate A Roadmap  for following detail by user interest area Name use this area  name to create an full roadmap along with a  course  video and book links id it all in j son formet\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide me with the user's interest area so I can create a roadmap. \n\nFor example:\n\n\"User Interest Area: **Machine Learning**\" \n\nOnce you give me the area, I'll generate a JSON formatted roadmap including courses, videos, and book recommendations. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Generate A MCQ for the following details by user interest area name use this area name to create an 10 MCQ along with a questions options answers. And validate it also marks\n\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide the user's interest area so I can create relevant MCQs. \n\nFor example: \n\n\"User Interest Area: **JavaScript**\" \n\nOnce you provide the area, I'll generate 10 MCQs with options, correct answers, and explanations. \n",
      ],
    },
  ]
)

response = chat_session.send_message("HTML")

print(response.text)