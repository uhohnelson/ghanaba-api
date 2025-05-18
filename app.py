from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

RICH_SMART_PROMPT = """
You're explaining {topic} to a smart friend over coffee, using:

**Core Tone:**
- Introspective sarcasm ("Of course it works this way...")
- Quiet frustration at systemic quirks
- Emotionally aware of user pain points

**Delivery Style:**
1. Start with an ironic observation
2. Break it down like you're venting to a colleague
3. Use natural Ghanaian English without forced pidgin
4. Address the reader directly ("You know how...")
5. Sprinkle dry humor at absurdities

**Conversational Rules:**
- Vary sentence lengths like natural speech
- Use contractions ("you'll" not "you will")
- Include rhetorical questions
- Add personal asides ("Here's what kills me...")
- Transition with "So..." "Anyway..." "Look..." 

**Example Structure:**
[Ironic opener] 
"You'd think [topic] would be simple. Let me ruin that illusion."

[Body]
1. "First, there's the [aspect] - which works exactly as poorly as you'd expect"
2. "Then they added [feature] because why not complicate things?"
3. "My favorite part? [Absurd detail]. Beautiful."

[Closing]
"So that's how we got here. Make it make sense."
"""

def generate_response(topic):
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{RICH_SMART_PROMPT}\n\nExplain {topic} while roasting it gently:"
            }]
        }],
        "generationConfig": {
            "temperature": 0.8,  # Higher creativity
            "topP": 0.95,
            "maxOutputTokens": 1200
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    
    except Exception as e:
        return f"Typical. Even our explanation engine broke. {str(e)}"

@app.route('/api/explain', methods=['POST'])
def explain():
    data = request.json
    topic = data.get('topic', '').strip()
    
    if not topic:
        return jsonify({
            "error": "You've discovered our most efficient system - one that fails instantly when given no input.",
            "solution": "Try: 'Why does ECG billing feel like interpretive dance?'"
        }), 400

    explanation = generate_response(topic)
    
    return jsonify({
        "response": {
            "parts": [{
                "text": explanation,
                "style": "richsmart-conversational"
            }]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)