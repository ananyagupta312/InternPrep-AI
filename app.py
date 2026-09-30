import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.gemini_service import GeminiConfigurationError, GeminiResponseError, analyze_with_gemini
from services.text_analyzer import analyze_resume_and_job

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200_000


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object with resume and job_description fields."}), 400

    resume = data.get("resume")
    job_description = data.get("job_description")
    if not isinstance(resume, str) or not resume.strip():
        return jsonify({"error": "Please add your resume text."}), 400
    if not isinstance(job_description, str) or not job_description.strip():
        return jsonify({"error": "Please add the job description."}), 400

    local_analysis = analyze_resume_and_job(resume, job_description)
    try:
        ai_analysis = analyze_with_gemini(resume, job_description, local_analysis)
    except GeminiConfigurationError:
        return jsonify({"error": "Gemini is not configured yet. Add your Google API key to the .env file."}), 503
    except GeminiResponseError:
        return jsonify({"error": "Gemini returned a response that could not be read. Please try again."}), 502
    except Exception:
        app.logger.exception("Gemini analysis failed")
        return jsonify({"error": "Gemini could not analyze this request. Please try again shortly."}), 502

    return jsonify({"local_analysis": local_analysis, "ai_analysis": ai_analysis})


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "The combined input is too large. Please keep it under 200 KB."}), 413


@app.errorhandler(Exception)
def unexpected_error(error):
    if isinstance(error, HTTPException):
        return jsonify({"error": error.description}), error.code
    app.logger.exception("Unexpected request error")
    return jsonify({"error": "Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")