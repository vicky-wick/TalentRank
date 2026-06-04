import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from modules.parser import extract_text_from_pdf
from modules.extractor import extract_experience_years, extract_certifications, extract_education, analyze_leadership, nlp
from modules.skills import extract_and_normalize_skills
from modules.embeddings import get_skill_embeddings
from modules.ats import calculate_ats_score, calculate_experience_score, calculate_cert_score, calculate_education_score, calculate_skill_score
from modules.comparison import compare_candidates

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def process_resume(filepath):
    text = extract_text_from_pdf(filepath)
    if not text:
        return None
        
    skills = extract_and_normalize_skills(text, nlp)
    years = extract_experience_years(text)
    certs = extract_certifications(text)
    edu = extract_education(text)
    
    # Calculate basic scores
    skill_score = calculate_skill_score(skills)
    exp_score = calculate_experience_score(years)
    cert_score = calculate_cert_score(certs)
    edu_score = calculate_education_score(edu)
    leadership_score = analyze_leadership(text)
    
    # Dummy evaluation for projects to avoid LLM calls
    project_score = 75
    
    ats_score = calculate_ats_score(
        skill_score=skill_score,
        experience_score=exp_score,
        project_score=project_score,
        certification_score=cert_score,
        education_score=edu_score,
        achievement_score=leadership_score
    )
    
    vector = get_skill_embeddings(skills)
    
    # Extract a short preview (first few non-empty lines) for identification
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    preview = ' | '.join(lines[:5])  # first 5 non-empty lines
    
    return {
        "text": text,
        "preview": preview[:300],
        "skills": skills,
        "years": years,
        "certs": certs,
        "edu": edu,
        "vector": vector,
        "scores": {
            "skill": skill_score,
            "experience": exp_score,
            "project": project_score,
            "certification": cert_score,
            "education": edu_score,
            "leadership": leadership_score
        },
        "ats_score": ats_score
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file_a = request.files.get("resume_a")
        file_b = request.files.get("resume_b")
        
        if file_a and file_b:
            path_a = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file_a.filename))
            path_b = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file_b.filename))
            
            file_a.save(path_a)
            file_b.save(path_b)
            
            data_a = process_resume(path_a)
            data_b = process_resume(path_b)
            
            if not data_a or not data_b:
                return "Error processing resumes. Please try again."
            
            data_a['filename'] = file_a.filename
            data_b['filename'] = file_b.filename
            
            comparison = compare_candidates(data_a, data_b)
            
            return render_template("result.html", data_a=data_a, data_b=data_b, comparison=comparison)
            
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
