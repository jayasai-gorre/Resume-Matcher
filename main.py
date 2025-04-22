from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Folder to save uploaded resumes
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --------------- Text Extraction Functions ---------------

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    return ""


# --------------- Routes ---------------

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/matcher", methods=["POST"])
def matcher():
    job_desc = request.form.get("job-desc")
    resume_files = request.files.getlist("resumes")

    if not job_desc or not resume_files:
        return render_template('index.html', message="Please upload resumes and enter a job description.")

    resumes_text = []
    filenames = []

    for resume_file in resume_files:
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(save_path)

        extracted_text = extract_text(save_path)
        resumes_text.append(extracted_text)
        filenames.append(resume_file.filename)

    vectorizer = TfidfVectorizer().fit_transform([job_desc] + resumes_text)
    vectors = vectorizer.toarray()

    job_vector = vectors[0]
    resume_vectors = vectors[1:]
    similarities = cosine_similarity([job_vector], resume_vectors)[0]

    top_indices = similarities.argsort()[-3:][::-1]
    top_resumes = [filenames[i] for i in top_indices]
    similarity_scores = [round(similarities[i], 2) for i in top_indices]

    return render_template("index.html", message="Top Matching Resumes:", topResumes=top_resumes, similarityScores=similarity_scores)


# --------------- Main Entry Point ---------------

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug_mode)
