import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Skills commonly found in software/AI job descriptions
SKILLS = {
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "node.js",
    "node",
    "flask",
    "django",
    "fastapi",
    "rest api",
    "api",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "power bi",
    "tableau",
    "excel",
    "linux",
    "agile",
    "rest",
    "oop",
    "object oriented programming",
}


def normalize_text(text):
    """
    Convert text to lowercase and remove unnecessary characters.
    """

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """
    Find known skills in the provided text.
    """

    text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:

        # Escape special regex characters
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)


def calculate_similarity(resume_text, job_description):
    """
    Calculate similarity between resume and job description
    using TF-IDF and cosine similarity.
    """

    documents = [
        normalize_text(resume_text),
        normalize_text(job_description)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def analyze_resume(resume_text, job_description):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matching_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    # Skill match percentage
    if len(job_skills) > 0:

        skill_match = (
            len(matching_skills)
            / len(job_skills)
        ) * 100

    else:

        skill_match = 0


    # Resume/JD similarity
    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )


    # Overall ATS score
    ats_score = (
        skill_match * 0.6
        +
        similarity_score * 0.4
    )

    ats_score = round(
        ats_score,
        2
    )


    return {
        "ats_score": ats_score,

        "skill_match": round(
            skill_match,
            2
        ),

        "similarity_score": similarity_score,

        "resume_skills": sorted(
            resume_skills
        ),

        "job_skills": sorted(
            job_skills
        ),

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,
    }