# Resume Matcher 🔍📝

A simple web application to match job descriptions with resumes using NLP (TF-IDF and Cosine Similarity). Upload multiple resumes and get the top matching ones based on the job description provided.

🌐 **Live Demo**: [Visit on Render](https://resume-matcher-6ovr.onrender.com/)

---

## 🚀 Features

- Upload multiple resumes in PDF, DOCX, or TXT format.
- Paste a job description.
- Get top 3 matching resumes with similarity scores.
- Built using Flask + Bootstrap.
- Responsive design with background image.
- Simple UI for real-world utility.

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **NLP**: Scikit-learn (TF-IDF + Cosine Similarity)
- **Hosting**: Render

---

## 📦 Installation (Local)

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/resume-matcher.git
   cd resume-matcher

2. **Create virtual environment**
   ```bash
    python -m venv myenv
    source myenv/bin/activate   # On Mac/Linux
    myenv\Scripts\activate      # On Windows
  
3. **Install dependencies**
   ```bash
    pip install -r requirements.txt

4. **Run the app**
   ```bash
   python main.py
