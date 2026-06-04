import spacy
import re
import datetime

# Attempt to load spacy model, if not, we assume it'll be installed and downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_experience_years(text):
    # Very basic regex to find date ranges and compute years
    # Format: Mon YYYY - Mon YYYY or Present
    matches = re.findall(r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4})\s*-\s*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|Present)', text, re.IGNORECASE)
    
    total_years = 0
    for start, end in matches:
        try:
            start_date = datetime.datetime.strptime(start[:3] + " " + start[-4:], '%b %Y')
            if end.lower() == 'present':
                end_date = datetime.datetime.now()
            else:
                end_date = datetime.datetime.strptime(end[:3] + " " + end[-4:], '%b %Y')
            
            diff = (end_date - start_date).days / 365.25
            if diff > 0:
                total_years += diff
        except Exception:
            continue
    
    # Fallback to simple regex if nothing found
    if total_years == 0:
        yr_matches = re.findall(r'(\d+)\+?\s*years? of experience', text, re.IGNORECASE)
        if yr_matches:
            total_years = sum([float(y) for y in yr_matches])
            
    return round(total_years, 2)

def extract_certifications(text):
    # Basic keyword matching for common certifications
    certs = ["aws certified", "azure certified", "azure fundamentals", "google cloud certified", "oracle certified", "ccna", "comptia", "pmp", "cism", "cissp"]
    found = []
    text_lower = text.lower()
    for c in certs:
        if c in text_lower:
            found.append(c)
    return found

def extract_education(text):
    edu = ["b.tech", "m.tech", "mba", "b.sc", "m.sc", "phd", "bachelor", "master"]
    found = []
    text_lower = text.lower()
    for e in edu:
        if e in text_lower:
            found.append(e)
    return found

def analyze_leadership(text):
    keywords = ["led", "managed", "mentored", "coordinator", "president", "team lead", "directed", "supervised"]
    score = 0
    text_lower = text.lower()
    for kw in keywords:
        if kw in text_lower:
            score += 15
    return min(100, score)
