
from app.text_cleaner import clean_text, extract_skills

resume = """
I am developing web applications using Python,
FastAPI, React, SQL, and Docker.
I have experience building REST APIs.
"""

print("Original text:")
print(resume)

print("\nCleaned text:")
print(clean_text(resume))

print("\nExtracted skills:")
print(extract_skills(resume))
