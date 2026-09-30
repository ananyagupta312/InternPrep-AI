import re

import pandas as pd

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "by", "for", "from",
    "has", "have", "in", "into", "is", "it", "its", "of", "on", "or", "our",
    "that", "the", "their", "this", "to", "using", "was", "were", "will", "with",
    "you", "your", "we", "they", "them", "i", "he", "she", "we", "what", "who",
    "when", "where", "why", "how", "work", "working", "role", "candidate", "team",
}

# Keep this list small and editable; aliases help recognize common wording variants.
SKILL_ALIASES = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "Express": ["express", "express.js", "expressjs"],
    "MongoDB": ["mongodb", "mongo db"],
    "MySQL": ["mysql", "my sql"],
    "Flask": ["flask"],
    "Django": ["django"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Git": ["git"],
    "GitHub": ["github", "git hub"],
    "REST APIs": ["rest api", "rest apis", "restful api", "restful apis"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "SQL": ["sql"],
    "Machine Learning": ["machine learning", "ml"],
    "Generative AI": ["generative ai", "gen ai"],
    "LLMs": ["llm", "llms", "large language model", "large language models"],
    "NLP": ["nlp", "natural language processing"],
    "Prompt Engineering": ["prompt engineering"],
    "OpenAI": ["openai"],
    "Gemini": ["gemini"],
    "LangChain": ["langchain"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
}


def preprocess_text(text):
    """Lowercase text, remove punctuation, tokenize, and discard stop words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS and not word.isdigit()]


def frequent_meaningful_words(text, limit=10):
    words = preprocess_text(text)
    if not words:
        return []
    counts = pd.Series(words).value_counts()
    return counts.head(limit).index.tolist()


def compare_important_words(resume, job_description):
    resume_words = set(frequent_meaningful_words(resume, limit=30))
    job_words = frequent_meaningful_words(job_description, limit=30)
    return [word for word in job_words if word in resume_words]


def extract_skills(text):
    found = []
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                found.append(skill)
                break
    return found


def analyze_resume_and_job(resume, job_description):
    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)
    resume_skill_set = set(resume_skills)
    matching_skills = [skill for skill in job_skills if skill in resume_skill_set]
    missing_skills = [skill for skill in job_skills if skill not in resume_skill_set]
    match_percentage = round(len(matching_skills) / len(job_skills) * 100) if job_skills else 0

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "matching_keywords": compare_important_words(resume, job_description),
    }