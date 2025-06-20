import os
import streamlit as st
import tempfile
from PyPDF2 import PdfReader
import cohere
from fpdf import FPDF

# Configure Cohere with your API key
cohere_api_key = "EVQzIdFzZWHbm9mjuaN6h0ed3Cq4iEOET3iyf1v6"
co = cohere.Client(cohere_api_key)

# Function to extract text from uploaded PDF
@st.cache_data
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    reader = PdfReader(tmp_file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    os.remove(tmp_file_path)
    return text

# Function to analyze the resume
def analyze_resume(resume_text, job_desc):
    prompt = f"""
    Analyze the following resume for the given job description and provide:
    1. A summary of strengths.
    2. Weaknesses or areas to improve.
    3. A score out of 100.

    Resume:
    {resume_text}

    Job Description:
    {job_desc}
    """

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=300,
        temperature=0.5
    )
    output = response.generations[0].text.strip()
    score = "N/A"
    for line in output.splitlines():
        if "score" in line.lower():
            score = line
            break
    return output, score

# Function to create PDF with feedback
def generate_feedback_pdf(feedback_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in feedback_text.split('\n'):
        try:
            pdf.cell(200, 10, txt=line.encode("latin-1", "replace").decode("latin-1"), ln=True)
        except:
            pdf.cell(200, 10, txt="[Encoding Error]", ln=True)
    pdf_output = "Resume_Feedback.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Streamlit Frontend
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI-Powered Resume Analyzer")
st.markdown("""
Upload your resume and the job description. Get instant AI-powered feedback to boost your chances of landing your dream job! ✨
""")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=100)
    st.markdown("### Instructions")
    st.markdown("""
    1. Upload your resume (PDF).
    2. Paste the job description.
    3. Click "Analyze".
    """)

uploaded_file = st.file_uploader("📎 Upload your resume (PDF)", type="pdf", key="resume_upload")
job_desc = st.text_area("💼 Paste the Job Description", height=150, key="job_desc_input")

if uploaded_file and job_desc:
    if st.button("🔍 Analyze My Resume", key="analyze_resume_btn"):
        with st.spinner("Analyzing your resume with AI..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            feedback, score = analyze_resume(resume_text, job_desc)

            st.success("✅ Analysis Complete!")
            st.markdown("### 📊 Resume Feedback:")
            st.write(feedback)
            st.markdown(f"**💯 Score:** {score}")

            pdf_path = generate_feedback_pdf(feedback)
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Download Feedback as PDF",
                    data=file,
                    file_name="Resume_Feedback.pdf",
                    mime="application/pdf",
                    key="download_pdf_btn"
                )
else:
    st.warning("Please upload your resume and paste the job description to proceed.")
