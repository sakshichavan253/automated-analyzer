from flask import Flask, render_template, request
import os
from parser import ResumeParser

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

parser = ResumeParser()


@app.route("/", methods=["GET", "POST"])
def index():
    data = None

    if request.method == "POST":
        file = request.files["resume"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            data = parser.parse_resume(filepath)

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)