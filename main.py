from flask import Flask, request, render_template
import os
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Creating a folder dynamically
app.config['UPLOAD_FOLDER'] = "uploads/"


# Extract text from pdf file
def extractTextFromPdfFile(filePath):
    text = ""
    with open(filePath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Extract text from docx file
def extractTextFromDocxFile(filePath):
    return docx2txt.process(filePath)

# Extract text from txt file
def extractTextFromTxtFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return file.read()

def extractText(filePath):
    if filePath.endswith(".pdf"):
        return extractTextFromPdfFile(filePath)
    elif filePath.endswith(".docx"):
        return extractTextFromDocxFile(filePath)
    elif filePath.endswith(".txt"):
        return extractTextFromTxtFile(filePath)
    else:
        return ""






# Route for rendering the html file
@app.route("/")
def matchresume():
    return render_template('index.html')


@app.route("/matcher", methods=['GET', 'POST'])
def matcher():
    if request.method == 'POST':

        # Getting the job-desc and resumes
        jobDesc = request.form.get('job-desc')
        resumeFiles = request.files.getlist('resumes')

        resumes = []
        for resumeFile in resumeFiles:

            # Storing the resume in the uploads dynamically
            fileName = os.path.join(app.config['UPLOAD_FOLDER'], resumeFile.filename)
            resumeFile.save(fileName)
            
            # Appending into the resumeList
            resumes.append(extractText(fileName))

        if not resumes and not jobDesc:
            return render_template('index.html', message="Please upload resumes and job post")
        

        '''
            Main Part of the Resume Matcher
        '''
        vectorizer = TfidfVectorizer().fit_transform([jobDesc] + resumes)
        vectors = vectorizer.toarray()
        jobVector = vectors[0]
        resumeVectors = vectors[1:]
        similarities = cosine_similarity([jobVector], resumeVectors)[0]


        topIndices = similarities.argsort()[-3:][::-1]
        topResumes = [resumeFiles[i].filename for i in topIndices]
        similarityScores = [round(similarities[i],2) for i in topIndices]


        # Now, return a result to the user (you could display the similarities)
        return render_template('index.html', message="Top Matching Resumes:", topResumes=topResumes, similarityScores=similarityScores)

    return render_template('index.html')  # Add this line to handle GET requests



if __name__=="__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)