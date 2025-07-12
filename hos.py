from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")


@app.route("/")
def serve_html():
    return send_file("HOSB.html")

@app.route("/HOSB.css")
def serve_css():
    return send_file("HOSB.css")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query.strip():
        return jsonify({"response": "Please enter a valid query."})

    try:
        response = model.generate_content(user_query)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error from Gemini API: {e}")  
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
