
import spacy
import json
from pathlib import Path

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Load the skills dictionary
SKILLS_FILE = Path(__file__).with_name("skills.json")

with open(SKILLS_FILE, "r", encoding="utf-8") as file:
    SKILLS = json.load(file)


def clean_text(text):
    """
    Convert text to lowercase,
    remove stopwords and punctuation,
    and lemmatize words.
    """
    doc = nlp(text.lower())

    cleaned_words = [
        token.lemma_
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
    ]

    return " ".join(cleaned_words)


def extract_skills(text):
    """
    Find skills from the original text
    using case-insensitive matching.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        skill_lower = skill.lower()
        start = 0

        while True:
            position = text_lower.find(skill_lower, start)

            if position == -1:
                break

            end = position + len(skill_lower)

            # Check boundaries so "C" does not match
            # the letter C inside another word.
            left_ok = (
                position == 0
                or not text_lower[position - 1].isalnum()
            )
            right_ok = (
                end == len(text_lower)
                or not text_lower[end].isalnum()
            )

            if left_ok and right_ok:
                found_skills.append(skill)
                break

            start = position + 1

    return found_skills
