from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_ghanaba_response(topic):
    return f"Ah {topic}? Okay make I break am down. Imagine say you dey Accra, and this thing happen like when ECG take light after you just buy cold minerals. That na the kind vibe we dey talk about. 😂"

@app.route('/explain', methods=['POST'])
def explain():
    data = request.json
    topic = data.get('topic', '')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    explanation = generate_ghanaba_response(topic)
    return jsonify({"response": explanation})

if __name__ == '__main__':
    app.run(debug=True)
