from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/hos1")
def hos1():
    return render_template("HOS1.html")
@app.route("/hmain")
def hmain():
    return render_template("Hmain.html")
@app.route("/win7")
def win7():
    return render_template("win7.html")
@app.route("/macos")
def macos():
    return render_template("macos.html")

@app.route("/win98")
def win98():
    return render_template("win98.html")
@app.route("/notes")
def notes():
    return render_template("fairynotes.html")

@app.route("/browser")
def browser():
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
DATA_FILE = "notes.json"

@app.route("/leave", methods=["POST"])
def leave_note():
    data = request.get_json()
    note = {
        "content": data.get("content", ""),
        "os": data.get("os", "hauntos")
    }

    notes = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            notes = json.load(f)

    notes.append(note)

    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)

    return jsonify({"message": "Note saved 👻"})

@app.route("/get-notes", methods=["GET"])
def get_notes():
    os_type = request.args.get("os", "hauntos")
    if not os.path.exists(DATA_FILE):
        return jsonify({"notes": []})
    with open(DATA_FILE, "r") as f:
        all_notes = json.load(f)
    filtered = [n for n in all_notes if n.get("os") == os_type]
    return jsonify({"notes": filtered})
if __name__ == "__main__":
    app.run(debug=True)
