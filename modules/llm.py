import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_related_skills(skill):
    prompt = f"What technologies and domains are related to {skill}? Return a JSON object with a single key 'related_skills' containing a list of strings."
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        return json.loads(text).get("related_skills", [])
    except Exception as e:
        print("LLM Error related skills:", e)
        return []

def evaluate_projects(resume_text):
    prompt = f"""
    Analyze the following resume text and evaluate the project complexity.
    Return a score between 1 and 100 for project quality.
    Return ONLY a JSON object like this:
    {{"project_score": 85}}
    
    Resume Text:
    {resume_text[:2000]}
    """
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text).get("project_score", 50)
    except Exception as e:
        print("LLM Error project score:", e)
        return 50

def llm_resume_evaluation(resume_text):
    prompt = f"""
    Analyze this resume text.
    Return a JSON object with these keys, each having a value from 0-100:
    "skill_strength", "experience_strength", "project_strength", "leadership_strength"
    
    Return ONLY valid JSON.
    
    Resume Text:
    {resume_text[:2000]}
    """
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text)
    except Exception as e:
        print("LLM Error evaluate resume:", e)
        return {
            "skill_strength": 50,
            "experience_strength": 50,
            "project_strength": 50,
            "leadership_strength": 50
        }
