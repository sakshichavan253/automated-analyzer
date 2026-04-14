import re
import json
import spacy
from pdfminer.high_level import extract_text
import docx

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load skills
with open("skills.json") as f:
    SKILLS_DB = [s.lower() for s in json.load(f)]


class ResumeParser:

    # -------- TEXT EXTRACTION --------
    def extract_text(self, file_path):
        if file_path.endswith(".pdf"):
            return extract_text(file_path)
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        return ""

    # -------- CLEAN TEXT --------
    def clean_text(self, text):
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # -------- EMAIL --------
    def extract_email(self, text):
        emails = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
        return emails[0] if emails else "Not Found"

    # -------- PHONE --------
    def extract_phone(self, text):
        phones = re.findall(r'\+?\d[\d\s\-]{8,15}', text)
        return phones[0] if phones else "Not Found"

    # -------- LINKEDIN --------
    def extract_linkedin(self, text):
        links = re.findall(r'https?://(?:www\.)?linkedin\.com/[^\s]+', text)
        return links[0] if links else "Not Found"

    # -------- NAME --------
    def extract_name(self, text):
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not Found"

    # -------- SKILLS --------
    def extract_skills(self, text):
        text_lower = text.lower()
        found = set()

        for skill in SKILLS_DB:
            if skill in text_lower:
                found.add(skill.title())

        return list(found)

    # -------- SECTION SEGMENT --------
    def segment_sections(self, text):
        sections = {
            "education": "",
            "experience": "",
            "projects": ""
        }

        lines = text.split("\n")
        current = None

        for line in lines:
            l = line.lower()

            if "education" in l:
                current = "education"
            elif "experience" in l or "work" in l:
                current = "experience"
            elif "project" in l:
                current = "projects"
            elif current:
                sections[current] += line + " "

        return sections

    # -------- FINAL PARSER --------
    def parse_file(self, file_path):
        raw_text = self.extract_text(file_path)
        clean = self.clean_text(raw_text)

        sections = self.segment_sections(raw_text)

        return {
            "name": self.extract_name(clean),
            "email": self.extract_email(clean),
            "phone": self.extract_phone(clean),
            "linkedin": self.extract_linkedin(clean),
            "skills": self.extract_skills(clean),
            "education": sections["education"].strip(),
            "experience": sections["experience"].strip(),
            "projects": sections["projects"].strip()
        }