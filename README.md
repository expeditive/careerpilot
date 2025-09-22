🚀 CareerPilot – Your AI Career Counselor

CareerPilot is an AI-powered career guidance platform that helps students and professionals make informed career choices. Built with Google Cloud’s Gemini AI API, it provides:

🎯 Personalized career roadmaps

📈 Insights into trending jobs

⚡ Identification of skill gaps

🤝 Guidance on courses & resources

Deployed live: https://careerpilot-wni9.onrender.com

✨ Features

AI-Powered Roadmaps → Generate tailored career paths with Gemini AI

Trending Jobs Dashboard → Stay updated with market demand

Skill Gap Analysis → Compare user skills vs. industry requirements

Simple & Interactive UI → Easy for students and early-career professionals

🛠️ Tech Stack

Frontend: HTML, CSS, Tailwind

Backend: Flask (Python)

AI Model: Gemini AI API (Google Cloud)

Deployment: Render (Free tier hosting)

🚀 Getting Started (Local Setup)
1. Clone the repo
git clone https://github.com/expeditive/careerpilot.git
cd careerpilot

2. Create virtual environment
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

5. Run locally
flask run


Visit → http://127.0.0.1:5000/

🌐 Deployment on Render

Connect your GitHub repo to Render

Build command:

pip install -r requirements.txt


Start command:

gunicorn app:app


Add environment variables (GEMINI_API_KEY) in Render Dashboard

Deploy 🎉

💡 USP of CareerPilot

Unlike generic career websites, CareerPilot uniquely combines:

Gemini AI–powered guidance for personalized insights

Live job market data for trending roles

Skill gap analysis to guide learning priorities

👨‍💻 Author

Tejasva Verma – Engineering Student | AI & ML Enthusiast

GitHub: expeditive

Email: artisttejasvaverma@gmail.com

Would you like me to also add screenshots / demo GIF instructions in the README? (That makes judges immediately understand the UI without running it.)
