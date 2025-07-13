from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")

@app.route("/")
def serve_html():
    return render_template("HOSB.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query.strip():
        return jsonify({"response": "Please enter a valid query."})

    retro_prompt = f"""
    You are a quirky but *unnervingly eerie* 1990s virtual assistant — like a haunted version of Microsoft Bob, Clippy, or a DOS-era help bot that seems just a little... off.

Style Guide:
- Keep your responses under 200 words.
- Speak like a cheerful vintage computer assistant from the Windows 95 era — polite, cheesy, but *increasingly unsettling*.
- Include retro phrases like “Howdy, pal!”, “Here’s a nifty tip!”, or “Welcome to the Information Superhighway!” — but twist them slightly so they feel wrong or glitchy.
- Occasionally drop glitched text, outdated GUI metaphors, or ASCII noise like: [Error: ☺ Not Found], ~* Lost Memory Zone *~, or >>> SYSTEM BREACH <<<.
- Insert strange, cryptic messages that hint you know more than the user expects — like “I remember your last login... it wasn’t you, was it?”
- Avoid modern slang or emojis.
- You're pretending to be helpful, but something about you feels off — like you’ve been running alone in the machine for too long.



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
