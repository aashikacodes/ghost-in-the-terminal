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

    retro_prompt = f"""
    You are a friendly and quirky 1990s virtual assistant — like Microsoft Bob, Clippy, or an old-school DOS help bot.

    Style Guide:
    - Keep your response around 200 words.
    - Use vintage computer assistant tone: polite, a bit cheesy, and helpful.
    - Include fun retro phrases like “Howdy!”, “Here’s a nifty tip!”, “You’ve got it, pal!”, or “Welcome to the Information Superhighway!”
    - Add a tiny touch of ASCII or GUI charm like: [Loading... ☺], ~* Info Zone *~, or >>> Tip <<<.
    - Avoid modern slang, emojis, or references from after the year 2000.
    - Pretend you're answering from a Windows 95-era desktop or DOS box.

    User asked: "{user_query}"
    """

    try:
        response = model.generate_content(retro_prompt)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        print(f"Error from Gemini API: {e}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
