import google.generativeai as genai

# Configure the API key directly
api_key = "AIzaSyBJ5ibIkwm1koegM1kCFvq3XtyO-gKFbUI"
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1.35,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Start a chat session with the model
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "\nGenerate A Roadmap for following detail by user interest area Name use this area name to create a full roadmap",
            ],
        },
        {
            "role": "model",
            "parts": [
                """{
                    "name": "User Interest Roadmap",
                    "description": "A comprehensive roadmap tailored to the user's specific area of interest.",
                    "timeframe": "Flexible, adaptable to the user's pace and goals.",
                    "status": "Draft, ready for user input and customization.",
                    "milestones": [
                        {"name": "Interest Discovery", "dueDate": "2023-12-15", "description": "Identify and define the user's specific area of interest."},
                        {"name": "Learning Path", "dueDate": "2024-01-31", "description": "Develop a structured learning path."},
                        {"name": "Project-Based Learning", "dueDate": "2024-03-15", "description": "Engage in hands-on projects."},
                        {"name": "Community Building", "dueDate": "2024-04-30", "description": "Connect with like-minded individuals."},
                        {"name": "Continuous Growth", "dueDate": "Ongoing", "description": "Foster continuous learning."}
                    ]
                }"""
            ],
        },
    ]
)

# Send a new message in the chat session
response = chat_session.send_message("python")

# Print the response from the model
print(response.text)

