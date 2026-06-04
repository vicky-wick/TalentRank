# TalentRank
AI-powered resume comparison and ATS scoring platform that ranks candidates using NLP, semantic embeddings, ESCO skill taxonomy, and LLM-powered analysis.

# AI Resume Matcher

An intelligent, side-by-side candidate comparison and resume scoring platform built using Flask, natural language processing (NLP), and vector embeddings. It parses PDF resumes, extracts key performance indicators (experience, education, leadership, certifications), maps technical skills using a standardized taxonomy, and performs semantic comparison.

---

## 🚀 Key Features

*   **PDF Extraction**: Automated text parsing using [PyMuPDF](https://pymupdf.readthedocs.io/).
*   **Skill Extraction & Normalization**:
    *   Identifies technical skills using standard NLP tokenization with [SpaCy](https://spacy.io/).
    *   Validates and normalizes skills against the extensive European Skills, Competences, Qualifications and Occupations (**ESCO**) taxonomy (`data/esco_skills.csv`).
    *   Expands unknown or emerging tech skills using **Google Gemini 3.5 Flash** to suggest related technologies and domains.
*   **Profile Feature Extractor**:
    *   **Years of Experience**: Computed dynamically via date range parser regex (including present-day calculation).
    *   **Education**: Detects degrees (e.g., B.Tech, M.Tech, MBA, Bachelor, Master, PhD).
    *   **Certifications**: Identifies standard credentials (e.g., AWS, Azure, CCNA, PMP, CISSP).
    *   **Leadership Score**: Scores candidates based on leadership verbs (e.g., *led*, *managed*, *mentored*, *directed*).
*   **Semantic Vector Comparison**:
    *   Embeds candidate skills using a local Sentence-Transformers model (`BAAI/bge-small-en-v1.5`).
    *   Calculates a **Skill Semantic Similarity** score between candidate profiles using **Cosine Similarity**.
*   **Automated ATS Scoring**: Matches resumes against typical corporate criteria using a weighted metric:
    *   **40%**: Technical Skills matching
    *   **25%**: Years of Experience
    *   **15%**: Projects Portfolio (powered by LLM project evaluation)
    *   **10%**: Leadership indicators
    *   **5%**: Certifications
    *   **5%**: Academic Education
*   **Side-by-Side Comparison UI**: Provides a clean web interface to upload files, displays progress, and renders a side-by-side comparison scorecard detailing overall winner, categorical results, and key recommendations.

---

## 🛠️ Tech Stack

*   **Backend**: Python, Flask, Werkzeug
*   **NLP & ML**: SpaCy (`en_core_web_sm`), Sentence-Transformers (`BAAI/bge-small-en-v1.5`), Scikit-learn
*   **LLM API**: Google Generative AI (Gemini 3.5 Flash)
*   **Data Processing**: Pandas, PyMuPDF (fitz)
*   **Frontend**: HTML5, Vanilla CSS, Bootstrap 5

---

## 📁 Project Structure

```text
resume_matcher/
├── app.py                  # Flask Application router & main processing flow
├── requirements.txt        # Python package dependencies
├── README.md               # Documentation
├── data/
│   ├── esco_skills.csv     # Standardized ESCO skills taxonomy dataset
│   └── skill_memory.json   # Cache database for normalized skill mappings
├── uploads/                # Temporary directory for uploaded resumes
├── templates/
│   ├── index.html          # Form page for uploading candidate resumes
│   └── result.html         # Comparison scorecard and detailed breakdown dashboard
└── modules/
    ├── parser.py           # Text extraction from PDF files
    ├── extractor.py        # Years of experience, certification, degree, and leadership parsers
    ├── skills.py           # Skill extraction and ESCO mapping logic
    ├── embeddings.py       # Sentence-transformers embedding vector generators
    ├── comparison.py       # Cosine similarity and categorical winner calculations
    ├── ats.py              # Score compilation and weighting algorithms
    └── llm.py              # Gemini LLM integration for skill expansion & project score
```

---

## ⚡ Getting Started

### Prerequisites

*   Python 3.9 or higher
*   Google Gemini API Key (if you wish to enable dynamically expanded skill mappings)

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd resume_matcher
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The application will automatically download the SpaCy `en_core_web_sm` English language model on its first run if it is not already present.*

3.  **Environment Setup**:
    Create a `.env` file in the root directory (or define the environment variable directly):
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

### Running the App

Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 📊 Evaluation Logic & Weights

The comparison system evaluates candidates using a combined scoring rubric:

| Metric | Calculation Method | Weight |
| :--- | :--- | :--- |
| **Skills** | Based on unique ESCO matched skills extracted from resume (10 pts per skill, max 100). | 40% |
| **Experience** | Computed from chronological date-ranges (<=1 yr: 40 pts, <=3 yrs: 80 pts, >3 yrs: 100 pts). | 25% |
| **Projects** | LLM-based complexity scoring evaluation of candidate projects. | 15% |
| **Leadership** | Counts leadership Action Verbs (15 pts per keyword, max 100). | 10% |
| **Education** | Based on number of degrees found (50 pts per degree, max 100). | 5% |
| **Certifications** | Counts detected professional certifications (30 pts per certification, max 100). | 5% |
