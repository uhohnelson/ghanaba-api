from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

PROMPT_TEMPLATES = {
    "serious": """Provide a concise, professional explanation of {topic}. 
    Focus on clarity and accuracy. Avoid humor or sarcasm.
    Structure:
    1. Definition
    2. Key components
    3. Practical implications""",
    
    "light": """Explain {topic} to a colleague with mild wit. 
    Use conversational language but remain professional.
    Example: "You'd think {topic} would be straightforward, but there are nuances..." """,
    
    "medium": """Explain {topic} with playful sarcasm and Ghanaian English flair. 
    Structure:
    - Ironic opener
    - Pain points delivered like a venting session
    - Dry closing remark ("So that's the mess we're in.")""",
    
    "heavy": """Roast {topic} aggressively. Assume the reader shares your frustration.
    Include:
    - Rhetorical questions ("Why does this still work this way?")
    - Dramatic pauses ("*sigh*")
    - Hyperbolic comparisons ("This is like trying to build IKEA furniture in the dark")"""
}

def generate_response(topic, tone="medium"):
    headers = {'Content-Type': 'application/json'}
    prompt = PROMPT_TEMPLATES.get(tone, PROMPT_TEMPLATES["medium"]).format(topic=topic)
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3 if tone == "serious" else 0.9,  # Low randomness for serious mode
            "maxOutputTokens": 1000
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error generating response. (API issue: {str(e)})"

@app.route('/api/explain', methods=['POST'])
def explain():
    data = request.json
    topic = data.get('topic', '').strip()
    tone = data.get('tone', 'medium').lower()  # Case-insensitive
    
    if not topic:
        return jsonify({"error": "Topic is required."}), 400
    
    valid_tones = ["serious", "light", "medium", "heavy"]
    if tone not in valid_tones:
        return jsonify({"error": f"Invalid tone. Choose from: {valid_tones}"}), 400

    explanation = generate_response(topic, tone)
    return jsonify({"response": explanation, "tone": tone})  # Include tone in response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)