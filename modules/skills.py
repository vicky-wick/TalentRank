import pandas as pd
import json
import os
from .llm import get_related_skills

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ESCO_PATH = os.path.join(DATA_DIR, "esco_skills.csv")
MEMORY_PATH = os.path.join(DATA_DIR, "skill_memory.json")

def load_esco():
    if os.path.exists(ESCO_PATH):
        df = pd.read_csv(ESCO_PATH)
        return set(df["label_cleaned"].str.lower().tolist())
    return set()

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=4)

esco_skills = load_esco()
skill_memory = load_memory()

# Common tech skills mapping
MAPPING = {
    "reactjs": "react",
    "react.js": "react",
    "node": "node.js",
    "js": "javascript",
    "golang": "go",
    "aws": "aws",
}

def extract_and_normalize_skills(text, nlp):
    """
    Very basic skill extraction based on named entities/nouns matching our dictionary.
    In a real scenario, this would use a robust NER model or a large skills dictionary.
    """
    doc = nlp(text)
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    
    # Basic bigram extraction
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    
    candidates = set(words + bigrams)
    
    extracted = set()
    
    for candidate in candidates:
        if candidate in MAPPING:
            extracted.add(MAPPING[candidate])
        elif candidate in esco_skills:
            extracted.add(candidate)
        else:
            # Simple heuristic for potential tech skills not in ESCO
            # For this MVP we will not call LLM for every single word. 
            pass

    # Let's say we have a specific list of skills extracted manually
    return list(set(extracted))

def process_unknown_skill(skill):
    skill_lower = skill.lower()
    if skill_lower in skill_memory:
        return skill_memory[skill_lower]
    
    # Call Gemini to get related skills
    related = get_related_skills(skill)
    if related:
        skill_memory[skill_lower] = related
        save_memory(skill_memory)
        return related
    return []
