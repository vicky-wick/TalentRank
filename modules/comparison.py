from sklearn.metrics.pairwise import cosine_similarity

def compare_candidates(a_data, b_data):
    # A vs B comparison logic
    
    sim_score = 0
    if a_data["vector"] is not None and b_data["vector"] is not None:
        sim_score = cosine_similarity([a_data["vector"]], [b_data["vector"]])[0][0] * 100
        
    categories = [
        ("Skills", a_data["scores"]["skill"], b_data["scores"]["skill"]),
        ("Experience", a_data["scores"]["experience"], b_data["scores"]["experience"]),
        ("Projects", a_data["scores"]["project"], b_data["scores"]["project"]),
        ("Certifications", a_data["scores"]["certification"], b_data["scores"]["certification"]),
        ("Education", a_data["scores"]["education"], b_data["scores"]["education"]),
        ("Leadership", a_data["scores"]["leadership"], b_data["scores"]["leadership"])
    ]
    
    table = []
    a_wins = 0
    b_wins = 0
    
    for cat, a_val, b_val in categories:
        winner = "A" if a_val > b_val else ("B" if b_val > a_val else "Tie")
        if winner == "A": a_wins += 1
        elif winner == "B": b_wins += 1
        
        table.append({
            "category": cat,
            "a": a_val,
            "b": b_val,
            "winner": winner
        })
        
    overall_winner = "Candidate A" if a_data["ats_score"] > b_data["ats_score"] else "Candidate B"
    if a_data["ats_score"] == b_data["ats_score"]:
        overall_winner = "Tie"
        
    reasons = []
    if a_data["ats_score"] > b_data["ats_score"]:
        if a_data["scores"]["skill"] > b_data["scores"]["skill"]: reasons.append("More relevant technical skills")
        if a_data["scores"]["project"] > b_data["scores"]["project"]: reasons.append("Stronger project portfolio")
        if a_data["scores"]["experience"] > b_data["scores"]["experience"]: reasons.append("Higher experience level")
        if a_data["scores"]["certification"] > b_data["scores"]["certification"]: reasons.append("Professional certifications")
    else:
        if b_data["scores"]["skill"] > a_data["scores"]["skill"]: reasons.append("More relevant technical skills")
        if b_data["scores"]["project"] > a_data["scores"]["project"]: reasons.append("Stronger project portfolio")
        if b_data["scores"]["experience"] > a_data["scores"]["experience"]: reasons.append("Higher experience level")
        if b_data["scores"]["certification"] > a_data["scores"]["certification"]: reasons.append("Professional certifications")
        
    return {
        "similarity": round(sim_score, 2),
        "table": table,
        "overall_winner": overall_winner,
        "reasons": reasons
    }
