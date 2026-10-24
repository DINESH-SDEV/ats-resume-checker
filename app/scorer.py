
import json
from pathlib import Path

from app.text_cleaner import clean_text, extract_skills
# Load synonym dictionary
SYNONYMS_FILE = Path(__file__).with_name("synonyms.json")

with open(SYNONYMS_FILE, "r", encoding="utf-8") as file:
    SYNONYMS = json.load(file)


def normalize_words(text):
    """Clean text and normalize known synonyms."""
    words = clean_text(text).split()
    normalized = []

    for word in words:
        normalized.append(SYNONYMS.get(word, word))

    return set(normalized)




def score_resume(resume_text, job_text):
    """Calculate a weighted resume match score."""

    resume_words = normalize_words(resume_text)
    job_words = normalize_words(job_text)

    matched_keywords = sorted(resume_words & job_words)
    missing_keywords = sorted(job_words - resume_words)

    # Technical skills receive higher importance
    resume_skills = {
        skill.lower() for skill in extract_skills(resume_text)
    }
    job_skills = {
        skill.lower() for skill in extract_skills(job_text)
    }

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    if not job_words:
        score = 0
    else:
        skill_words = {
            word
            for skill in job_skills
            for word in normalize_words(skill)
        }

        # Give skill-related keywords weight 2,
        # other keywords weight 1.
        total_weight = sum(
            2 if word in skill_words else 1
            for word in job_words
        )

        matched_weight = sum(
            2 if word in skill_words else 1
            for word in matched_keywords
        )

        score = round(
            matched_weight / total_weight * 100,
            2
        )

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
