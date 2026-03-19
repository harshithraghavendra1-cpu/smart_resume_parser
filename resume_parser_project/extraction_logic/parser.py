import fitz  # PyMuPDF
import docx
import re
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# -------------------------------
# TEXT EXTRACTION FUNCTIONS
# -------------------------------

def extract_text(file):
    text = ""

    # PDF handling
    if file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()

    # DOCX handling
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# -------------------------------
# INFORMATION EXTRACTION
# -------------------------------

def extract_info(text):
    doc = nlp(text)

    # 📧 EMAIL
    email = re.findall(r'\S+@\S+', text)

    # 📱 PHONE
    phone = re.findall(r'\+?\d[\d\s-]{8,}', text)

    # 🛠 SKILLS (custom list - you can expand)
    skills_list = [
        "python", "java", "c++", "machine learning",
        "data science", "sql", "html", "css",
        "javascript", "react", "node", "django"
    ]

    skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills.append(skill)

    # 🎓 EDUCATION
    education = re.findall(
        r"(b\.tech|m\.tech|bachelor|master|b\.sc|m\.sc|degree)",
        text.lower()
    )

    # 💼 EXPERIENCE (years)
    experience = re.findall(r"(\d+)\+?\s+years", text.lower())

    # 🧠 NAME (using spaCy NER)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience
    }
