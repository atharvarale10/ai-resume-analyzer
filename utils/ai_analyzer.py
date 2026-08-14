import os
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert technical recruiter and resume evaluator.

Analyze the candidate's resume against the provided job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Evaluate the candidate ONLY using information present in the resume.

Provide the following sections:

1. ATS Match Score
Give a score from 0 to 100.

2. Matching Skills
List skills from the job description that are clearly present
in the resume.

3. Missing Skills
List important skills from the job description that are missing
or not clearly demonstrated.

4. Strengths
List the strongest aspects of the resume for this job.

5. Weaknesses
List areas where the resume could be improved.

6. Recommendations
Give practical suggestions for improving the resume.

7. Keywords
List important keywords from the job description that the
candidate should consider including IF they genuinely possess
those skills.

IMPORTANT:
Do not invent skills, experience, education, certifications,
projects, or achievements that are not present in the resume.
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text