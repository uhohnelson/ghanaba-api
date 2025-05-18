from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Enable cross-origin requests
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ This allows your frontend (even from file:// or localhost) to connect

# Gemini API setup
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')  # Must be set in Render environment
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Generate response using Gemini
def generate_ghanaba_response(topic):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Explain {topic} in a fun Ghanaian style like Ghanaba would."}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            generated_text = data['candidates'][0]['content']
            return generated_text
        except (KeyError, IndexError):
            return "Sorry, no explanation was generated."
    else:
        return f"Error from Gemini API: {response.status_code} - {response.text}"

# POST endpoint for explanations
@app.route('/api/explain', methods=['POST'])
def explain():
    data = request.json
    topic = data.get('topic', '')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    explanation = generate_ghanaba_response(topic)
    return jsonify({"response": explanation})

# Root route
@app.route('/')
def home():
    return "Welcome to Ghanaba API. It's alive!"

# Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
