import google.generativeai as genai

# Configure Google Generative AI SDK with your API key
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
                "Generate a roadmap for the following detail by user interest area. Use this area name to create a full roadmap along with course, video, and book links.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Please provide me with the user's interest area! I need to know what they're interested in before I can create a roadmap. \n\nFor example, tell me:\n* **\"The user is interested in Data Science.\"** \n* **\"The user wants to learn about Game Development.\"**\n* **\"The user's interest area is Digital Marketing.\"**\n\nOnce you give me that information, I can generate a full roadmap with course, video, and book recommendations! 📚 \n",
            ],
        },
    ]
)

response = chat_session.send_message("Python")

print(response.text)
