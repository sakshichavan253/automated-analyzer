from flask import Flask, render_template, request
import os
from parser import ResumeParser

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "docx"}

parser = ResumeParser()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":

        if "resume" not in request.files:
            error = "No file uploaded"
            return render_template("index.html", result=result, error=error)

        file = request.files["resume"]

        if file.filename == "":
            error = "No file selected"
            return render_template("index.html", result=result, error=error)

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ensure folder exists
            file.save(filepath)

            result = parser.parse_file(filepath)
        else:
            error = "Only PDF and DOCX files allowed"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=10000)