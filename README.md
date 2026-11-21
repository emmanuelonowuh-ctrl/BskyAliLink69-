import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Shopify AI Agent is Live!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    # Simple AI reply - you can connect OpenAI later
    reply = f"I got your message: '{msg}'. How can I help with your Shopify store? I can help with products, orders, and discounts."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
