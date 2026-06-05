# TalentRank

AI-powered resume comparison and ATS scoring platform that ranks candidates using NLP, semantic embeddings, ESCO skill taxonomy, and LLM-powered analysis.
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

## 📊 Evaluation Logic, Methods & Weights

### 1. ATS Numerical Score Computation
The system computes an overall **ATS Score (out of 100)** for each candidate using a weighted sum of individual metric scores:

$$\text{ATS Score} = (0.40 \times \text{Skill Score}) + (0.25 \times \text{Experience Score}) + (0.15 \times \text{Project Score}) + (0.10 \times \text{Leadership Score}) + (0.05 \times \text{Certification Score}) + (0.05 \times \text{Education Score})$$

#### Categorical Score Metrics:
*   **Skills Score (40% Weight)**:
    *   Calculated as: $\min(100, \text{number of skills} \times 10)$
*   **Experience Score (25% Weight)**:
    *   $\le 0$ years: $20\text{ pts}$
    *   $\le 1$ year: $40\text{ pts}$
    *   $\le 3$ years: $80\text{ pts}$
    *   $> 3$ years: $100\text{ pts}$
*   **Project Score (15% Weight)**:
    *   Evaluates project complexity (rated from $1\text{ to }100$, defaults to $75\text{ for MVP}$).
*   **Leadership Score (10% Weight)**:
    *   Analyzes presence of leadership action verbs (e.g. *led*, *managed*, *mentored*, *directed*), scoring $15\text{ pts}$ per unique verb up to a maximum of $100\text{ pts}$.
*   **Education Score (5% Weight)**:
    *   Calculated as: $\min(100, \text{number of degrees} \times 50)$
*   **Certification Score (5% Weight)**:
    *   Calculated as: $\min(100, \text{number of certifications} \times 30)$

---

### 2. Semantic Similarity Score (Cosine Similarity)
To perform side-by-side profile comparisons, the system measures the semantic overlap between the candidates' skill profiles:

#### Embedding Generation:
1. Candidate skills are extracted and normalized against the ESCO database.
2. Each individual skill is embedded into a dense vector space using a local `BAAI/bge-small-en-v1.5` SentenceTransformer model (producing 384-dimensional vectors).
3. The individual skill embeddings are averaged (mean pooled) to represent the candidate's complete profile vector $\mathbf{u}$ (or $\mathbf{v}$):
   $$\mathbf{u} = \frac{1}{N}\sum_{i=1}^{N}\text{embedding}(\text{skill}_i)$$

#### Similarity Calculation:
We compute the **Cosine Similarity** between the averaged profile vectors of Candidate A ($\mathbf{u}$) and Candidate B ($\mathbf{v}$), and scale the result to a percentage ($0\text{ to }100\%$):

$$\text{Similarity Score} = \text{cosine\_similarity}(\mathbf{u}, \mathbf{v}) \times 100 = \left( \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} \right) \times 100$$

Where:
*   $\mathbf{u} \cdot \mathbf{v}$ is the dot product of the two vectors.
*   $\|\mathbf{u}\|$ and $\|\mathbf{v}\|$ are the Euclidean norms (magnitudes) of the vectors.

