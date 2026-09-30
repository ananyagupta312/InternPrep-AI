import json
import os

from google import genai

from prompts import build_analysis_prompt

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "relevant_strengths": {"type": "ARRAY", "items": {"type": "STRING"}},
        "missing_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
        "project_relevance": {"type": "ARRAY", "items": {"type": "STRING"}},
        "resume_suggestions": {"type": "ARRAY", "items": {"type": "STRING"}},
        "interview_questions": {"type": "ARRAY", "items": {"type": "STRING"}},
        "overall_analysis": {"type": "STRING"},
    },
    "required": [
        "relevant_strengths",
        "missing_skills",
        "project_relevance",
        "resume_suggestions",
        "interview_questions",
        "overall_analysis",
    ],
}


class GeminiConfigurationError(Exception):
    pass


class GeminiResponseError(Exception):
    pass


def _validate_analysis(data):
    if not isinstance(data, dict):
        raise GeminiResponseError("Gemini response was not a JSON object")

    expected_lists = [
        "relevant_strengths",
        "missing_skills",
        "project_relevance",
        "resume_suggestions",
        "interview_questions",
    ]
    if any(not isinstance(data.get(key), list) or not all(isinstance(item, str) for item in data[key]) for key in expected_lists):
        raise GeminiResponseError("Gemini response had an unexpected structure")
    if not 5 <= len(data["interview_questions"]) <= 8:
        raise GeminiResponseError("Gemini response did not include 5 to 8 interview questions")
    if not isinstance(data.get("overall_analysis"), str):
        raise GeminiResponseError("Gemini response had an unexpected structure")

    return {key: data[key] for key in (*expected_lists, "overall_analysis")}


def analyze_with_gemini(resume, job_description, local_analysis):
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GEMINI_MODEL")
    if not api_key or not model:
        raise GeminiConfigurationError("GOOGLE_API_KEY and GEMINI_MODEL are required")

    client = genai.Client(api_key=api_key)
    response = client.interactions.create(
        model=model,
        input=build_analysis_prompt(resume, job_description, local_analysis),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": RESPONSE_SCHEMA,
        },
        generation_config={"temperature": 0.3},
    )
    try:
        parsed = json.loads(response.output_text)
    except (TypeError, json.JSONDecodeError) as error:
        raise GeminiResponseError("Gemini did not return valid JSON") from error
    return _validate_analysis(parsed)