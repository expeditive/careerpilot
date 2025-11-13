# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "iloveyou"  # For session management

# --- Gemini setup ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ Google API key not found. Make sure it's in .env as GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")

# --------------------- ROUTES ---------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/input", methods=["GET"])
def input_form():
    return render_template('input.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    import json, re

    form_data = []
    for key, value in request.form.items():
        form_data.append(f"{key}: {value}")

    skills = request.form.getlist('skills')
    interests = request.form.getlist('interests')

    if skills:
        form_data.append(f"skills: {', '.join(skills)}")
    if interests:
        form_data.append(f"interests: {', '.join(interests)}")

    prompt = (
        "You are an AI career counsellor. Based on this user profile, return ONLY valid JSON "
        "with the following structure (no explanations, no markdown, no commentary):\n\n"
        "{\n"
        "  \"career_paths\": [{\"title\": \"\", \"why_fit\": \"\"}],\n"
        "  \"roadmap\": [{\"title\": \"\", \"details\": \"\"}],\n"
        "  \"courses\": [{\"name\": \"\", \"details\": \"\"}],\n"
        "  \"trending_jobs\": [{\"title\": \"\", \"description\": \"\"}],\n"
        "  \"skills_to_focus\": [{\"skill\": \"\", \"reason\": \"\"}],\n"
        "  \"companies_hiring\": [{\"company\": \"\", \"reason\": \"\"}]\n"
        "}\n\n"
        "Analyze this user:\n" + "\n".join(form_data)
    )

    data = {}

    try:
        print("---- Sending prompt to Gemini ----")
        result = model.generate_content(prompt)
        if not result:
            print("⚠️ No response object returned by Gemini.")
        else:
            print("---- RAW GEMINI RESPONSE ----")
            print(result.text)
            print("-----------------------------")

        raw_response = result.text if result and result.text else "{}"

        # Extract JSON (including ```json wrappers)
        match = re.search(r"```json\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
        if match:
            raw_json = match.group(1)
        else:
            match = re.search(r"\{.*\}", raw_response, re.DOTALL)
            raw_json = match.group(0) if match else "{}"

        try:
            data = json.loads(raw_json)
        except Exception as e:
            print("⚠️ JSON decode failed:", e)
            print("Raw attempted JSON:", raw_json)
            data = {}

    except Exception as e:
        print("⚠️ Exception during Gemini call:", e)
        data = {"error": f"Error contacting Gemini: {e}"}

    session["roadmap_data"] = data
    return redirect(url_for("roadmap"))


@app.route('/roadmap')
def roadmap():
    data = session.get("roadmap_data", {})
    return render_template("roadmap.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
