def calculate_ats_score(skill_score, experience_score, project_score, certification_score, education_score, achievement_score):
    """
    0.40 * skill_score +
    0.25 * experience_score +
    0.15 * project_score +
    0.05 * certification_score +
    0.05 * education_score +
    0.10 * achievement_score
    """
    ats = (0.40 * skill_score) + \
          (0.25 * experience_score) + \
          (0.15 * project_score) + \
          (0.05 * certification_score) + \
          (0.05 * education_score) + \
          (0.10 * achievement_score)
          
    return round(ats, 2)

def calculate_experience_score(years):
    if years <= 0: return 20
    elif years <= 1: return 40
    elif years <= 3: return 80
    else: return 100

def calculate_cert_score(certs):
    score = len(certs) * 30
    return min(100, score)

def calculate_education_score(edu):
    score = len(edu) * 50
    return min(100, score)

def calculate_skill_score(skills):
    # Base score on number of skills for MVP
    score = len(skills) * 10
    return min(100, score)
