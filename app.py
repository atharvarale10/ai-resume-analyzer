from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import fitz

from utils.ats_analyzer import analyze_resume


app = Flask(__name__)

# Folder where uploaded resumes will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Only allow PDF files
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_text_from_pdf(filepath):
    text = ""

    pdf = fitz.open(filepath)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check whether a file was submitted
    if "resume" not in request.files:
        return "No resume file uploaded."

    resume = request.files["resume"]

    # Get job description
    job_description = request.form.get("job_description")

    # Check whether user selected a file
    if resume.filename == "":
        return "No file selected."

    # Check file type
    if not allowed_file(resume.filename):
        return "Only PDF files are allowed."

    # Make filename safe
    filename = secure_filename(resume.filename)

    # Save the file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(filepath)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(filepath)

    # Send resume + job description to AI
    analysis = analyze_resume(
        resume_text,
        job_description
    )

    # Display results
    return render_template(
        "result.html",
        resume_text=resume_text,
        analysis=analysis
    )


if __name__ == "__main__":
    app.run(debug=True)