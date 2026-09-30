# InternPrep AI

## About

A simple AI-powered tool that helps students compare their resumes with internship and job descriptions. The skill percentage comes from local text matching; Gemini provides the written feedback.

## Features

- Resume and JD comparison
- Basic NLP-based skill extraction
- Skill overlap calculation
- Gemini-powered resume analysis
- Missing skill identification
- Resume improvement suggestions
- Role-specific interview questions

## Tech Stack

Python, Flask, Google Gemini API, Pandas, HTML, CSS, and JavaScript.

## How It Works

```text
Resume + Job Description
        ↓
Basic Text Processing
        ↓
Skill Extraction
        ↓
Skill Matching
        ↓
Gemini Analysis
        ↓
Results
```

Text preprocessing lowercases text, removes punctuation, splits it into word tokens, and ignores a small list of common stop words. Pandas counts frequent meaningful words, which are compared between the resume and JD. A predefined skill list separately recognizes technologies in each input. The local match percentage is matching recognized JD skills divided by all recognized JD skills; it is 0 when the JD has no recognized skills. This is text processing, not a machine-learning model or a prediction of hiring chances.

The app sends the local analysis and both text inputs to Gemini for a separate written review. Gemini is asked for JSON fields that the backend validates before returning them to the page. Pandas is used to count the most frequent meaningful words during local preprocessing.

## Setup

On Windows, from the project folder:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder (or edit the included one) and add your Google AI Studio API key:

```text
GOOGLE_API_KEY=your_real_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Keep `.env` private; it is ignored by Git. Start Flask:

```powershell
python app.py
```

Open the local URL printed by Flask, usually `http://127.0.0.1:5000`.

## Main Files

- `app.py` serves the page and exposes `/health` and `/analyze` JSON routes.
- `services/text_analyzer.py` handles local text processing, skill extraction, and the transparent percentage calculation.
- `services/gemini_service.py` calls the Google Gen AI SDK and validates Gemini's JSON response.
- `prompts.py` contains the instructions sent with resume, JD, and local-analysis data.
- `templates/index.html`, `static/style.css`, and `static/script.js` make up the browser interface.

The browser sends a `fetch()` POST request to Flask. Flask returns JSON with `local_analysis` and `ai_analysis`, which JavaScript displays without reloading the page.