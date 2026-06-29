import PyPDF2
import pdfplumber
from docx import Document
import re


# -------------------------------
# TEXT EXTRACTION FUNCTIONS
# -------------------------------

def extract_text_from_pdf(file):
    text = ""

    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"PyPDF2 error: {e}")

    # fallback to pdfplumber
    if not text:
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"pdfplumber error: {e}")

    return text


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


# -------------------------------
# CLEANING FUNCTION
# -------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s@.+#-]', '', text)

    return text.strip()


# -------------------------------
# MAIN TEXT WRAPPER (IMPORTANT)
# -------------------------------

def extract_text(file):
    if file.name.endswith('.pdf'):
        text = extract_text_from_pdf(file)

    elif file.name.endswith('.docx'):
        text = extract_text_from_docx(file)

    else:
        return ""

    return clean_text(text)


# -------------------------------
# SKILL EXTRACTION
# -------------------------------

SKILLS_DB = [
    "python", "django", "react", "sql",
    "machine learning", "data analysis",
    "java", "c++", "aws", "azure"
]


def extract_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------------
# EXPERIENCE EXTRACTION
# -------------------------------

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+years?', text)

    if matches:
        return max([int(m) for m in matches])

    return 0


# -------------------------------
# EDUCATION EXTRACTION
# -------------------------------

def extract_education(text):
    education_keywords = [
        "bachelor", "master", "bsc", "msc",
        "btech", "mtech", "mca"
    ]

    found = []

    for edu in education_keywords:
        if edu in text:
            found.append(edu)

    return list(set(found))


# def parse_resume(file):
#     text = extract_text(file)

#     return {
#         "skills": extract_skills(text),
#         "experience_years": extract_experience(text),
#         "education": extract_education(text)
#     }

# -------------------------------
# PARSE FROM TEXT (OPTIMIZED)
# -------------------------------

def parse_resume_from_text(text):
    return {
        "skills": extract_skills(text),
        "experience_years": extract_experience(text),
        "education": extract_education(text)
    }