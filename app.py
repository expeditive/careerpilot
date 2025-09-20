
# app.py
from flask import Flask, render_template, request, redirect,url_for, session
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = "iloveyou"  # For session management


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("⚠️ Google API key not found. Make sure it's in .env as GOOGLE_API_KEY")

# ✅ Correct usage
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/input", methods=["GET"])
def input_form():
    return render_template('input.html')

@app.route('/submit', methods=['POST'])
def submit_form():
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
        "You are an AI career counsellor. Based on this profile, provide a structured JSON response with the following sections:\n\n"
        "1. career_paths → 5–6 suitable career paths (title + why fit)\n"
        "2. roadmap → step-by-step plan for 2–3 years (title + details)\n"
        "3. courses → recommended online courses or projects (name + details)\n"
        "4. trending_jobs → top trending job roles in their suited field (title + description)\n"
        "5. skills_to_focus → 5 most important skills they must learn (skill + why important)\n"
        "6. companies_hiring → notable companies hiring in their field (company + reason)\n\n"
        "⚠️ Respond ONLY in valid JSON.\n\n"
        + "\n".join(form_data)
    )


    import json

    try:
        result = model.generate_content(prompt)
        raw_response = result.text if result and result.text else "{}"

        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError:
            # If Gemini wrapped JSON in ```json ... ```
            raw = raw_response.split("```json")[-1].split("```")[0]
            data = json.loads(raw)

    except Exception as e:
        data = {"error": f"⚠️ Error while contacting Gemini: {str(e)}"}

    session["roadmap_data"] = data


    # Store structured info
    session["x"] = data
    return redirect(url_for("roadmap"))

import markdown

@app.route('/roadmap')
def roadmap():
    data = session.get("roadmap_data", {})
    return render_template("roadmap.html", data=data)






if __name__ == '__main__':
    app.run(debug=True)