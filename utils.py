# utils.py
import cohere
import os
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def analyze_resume(resume_text, job_description):
    prompt = f"""You are a resume reviewer. The candidate's resume is:
{resume_text}

The job description is:
{job_description}

Rate how well the resume matches the job (score out of 100), and give 3 suggestions to improve it."""
    
    response = co.generate(
        model="command-r",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    return response.generations[0].text.strip()
