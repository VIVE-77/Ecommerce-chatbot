from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Replace with your own key securely
)

def get_response_from_deepseek(user_message):
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost:5500",
            "X-Title": "Smart E-Commerce Assistant"
        },
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": user_message}]
    )
    return completion.choices[0].message.content

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please enter a message!"})
    reply = get_response_from_deepseek(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
