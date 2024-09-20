
import google.generativeai as genai

api_key = "AIzaSyBJ5ibIkwm1koegM1kCFvq3XtyO-gKFbUI"
genai.configure(api_key=api_key)


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
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)