from flask import Flask, render_template, request
import os
from parser import ResumeParser

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf", "docx"}

parser = ResumeParser()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":

        # Check file present
        if "resume" not in request.files:
            error = "No file uploaded"
            return render_template("index.html", result=result, error=error)

        file = request.files["resume"]

        # Check file selected
        if file.filename == "":
            error = "No file selected"
            return render_template("index.html", result=result, error=error)

        # Check file type
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            result = parser.parse_file(filepath)
        else:
            error = "Only PDF and DOCX files allowed"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)