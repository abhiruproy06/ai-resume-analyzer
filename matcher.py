import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "mysql",
    "postgresql",
    "data structures",
    "algorithms",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "fastapi",
    "flask",
    "django",
    "git",
    "github",
    "docker",
    "aws",
    "linux",
    "cybersecurity",
    "networking",
    "operating systems",
    "database management",
    "problem-solving",
]

def get_semantic_model():
    """Load a pretrained sentence-embedding model."""
    return SentenceTransformer("all-MiniLM-L6-v2")
from functools import lru_cache


@lru_cache(maxsize=1)
def get_semantic_model():
    """Load and cache the semantic similarity model."""
    return SentenceTransformer("all-MiniLM-L6-v2")


def normalize_text(text):
    """Normalize text before comparison."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def detect_skills(text):
    """Detect known skills mentioned in text."""
    normalized = normalize_text(text)
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized):
            found.append(skill)

    return found


def analyze_resume(resume_text, job_description):
    """Compare a resume with a job description."""

    resume_clean = normalize_text(resume_text)
    job_clean = normalize_text(job_description)

    if not resume_clean or not job_clean:
        raise ValueError(
            "Resume and job description cannot be empty."
        )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        [resume_clean, job_clean]
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]
    model = get_semantic_model()

    embeddings = model.encode(
        [resume_clean, job_clean],
        normalize_embeddings=True
    )

    semantic_score = float(
        cosine_similarity(
            embeddings[0:1],
            embeddings[1:2]
        )[0][0]
    )

    semantic_score = max(0.0, min(100.0, semantic_score * 100))

    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_description)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:
        skill_coverage = len(matched_skills) / len(job_skills)
    else:
        skill_coverage = None

    results = {
        "similarity_score": round(similarity * 100, 1),
        "semantic_score": round(semantic_score, 1),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_coverage": (
            round(skill_coverage * 100, 1)
            if skill_coverage is not None
            else None
        ),
    }

    return results