import re
import spacy
from pdfminer.high_level import extract_text
from docx import Document
import json

nlp = spacy.load("en_core_web_sm")


class ResumeParser:

    def extract_text(self, file_path):
        if file_path.endswith(".pdf"):
            return extract_text(file_path)

        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])

        return ""

    # ---------------- NAME ----------------
    def extract_name(self, text):
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not Found"

    # ---------------- EMAIL ----------------
    def extract_email(self, text):
        match = re.search(r"\S+@\S+", text)
        return match.group() if match else "Not Found"

    # ---------------- PHONE ----------------
    def extract_phone(self, text):
        match = re.search(r"\+?\d[\d\s-]{8,}", text)
        return match.group() if match else "Not Found"

    # ---------------- LINKEDIN ----------------
    def extract_linkedin(self, text):
        match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+", text)
        return match.group() if match else "Not Found"

    # ---------------- SKILLS ----------------
    def extract_skills(self, text):
        with open("skills.json") as f:
            skills_data = json.load(f)

        found_skills = []
        for skill in skills_data["skills"]:
            if skill.lower() in text.lower():
                found_skills.append(skill)

        return found_skills

    # ---------------- EDUCATION ----------------
    def extract_education(self, text):
        lines = text.split("\n")
        education = []

        keywords = ["bachelor", "master", "bca", "btech", "mca", "mba", "college", "university"]

        for line in lines:
            if any(word in line.lower() for word in keywords):
                education.append(line.strip())

        return education if education else ["Not Found"]

    # ---------------- EXPERIENCE ----------------
    def extract_experience(self, text):
        lines = text.split("\n")
        experience = []

        keywords = ["experience", "intern", "worked", "company", "job"]

        for line in lines:
            if any(word in line.lower() for word in keywords):
                experience.append(line.strip())

        return experience if experience else ["Not Found"]

    # ---------------- PROJECTS ----------------
    def extract_projects(self, text):
        lines = text.split("\n")
        projects = []

        keywords = ["project", "developed", "built", "created"]

        for line in lines:
            if any(word in line.lower() for word in keywords):
                projects.append(line.strip())

        return projects if projects else ["Not Found"]

    # ---------------- FINAL ----------------
    def parse_resume(self, file_path):
        text = self.extract_text(file_path)

        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "linkedin": self.extract_linkedin(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "projects": self.extract_projects(text)
        }