import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def calculate_ats_score(resume_text: str, job_description: str):
    """Calculate ATS score and keyword matching between resume and job description."""
    vectorizer = CountVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([job_description, resume_text])
    job_vec, resume_vec = vectors[0], vectors[1]
    similarity = cosine_similarity(job_vec, resume_vec)[0][0]
    job_tokens = vectorizer.get_feature_names_out()
    resume_counts = resume_vec.toarray()[0]
    matching = [token for token, count in zip(job_tokens, resume_counts) if count > 0]
    missing = [token for token, count in zip(job_tokens, resume_counts) if count == 0]
    score = round(similarity * 100, 2)
    return score, matching, missing

def tailor_resume(resume_text: str, job_description: str, missing_keywords, client) -> str:
    prompt = f"""You are an expert resume writer.\nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nImprove the resume to better match the job description.\nInclude the following missing keywords where relevant: {', '.join(missing_keywords)}\nReturn an ATS-optimized version of the resume."""
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[{"role": "system", "content": prompt}],
    )
    return response.choices[0].message.content


def main():
    st.title("ATS Resume Checker")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Job Description")
    if uploaded_file and job_desc:
        resume_text = extract_text_from_pdf(uploaded_file)
        score, matched, missing = calculate_ats_score(resume_text, job_desc)
        st.metric("ATS Score", f"{score}%")
        st.write("**Matched Keywords:**", ", ".join(matched) if matched else "None")
        st.write("**Missing Keywords:**", ", ".join(missing) if missing else "None")
        if missing and st.button("Tailor Resume"):
            api_key = st.secrets.get("DEEPSEEK_API_KEY")
            if not api_key:
                st.warning("API key not configured in Streamlit secrets.")
            else:
                client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                tailored = tailor_resume(resume_text, job_desc, missing, client)
                st.text_area("Tailored Resume", value=tailored, height=400)


if __name__ == "__main__":
    main()
