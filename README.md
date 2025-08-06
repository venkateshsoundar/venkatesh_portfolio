# venkatesh_portfolio
This Project covers the code for my professional portfolio development

## ATS Resume Checker

A Streamlit tool to compare a resume against a job description and estimate an ATS score.
Upload a PDF resume and paste the job description to see keyword matches, missing terms, and generate an ATS‑optimized version of the resume.

To enable resume tailoring, place an OpenRouter API key in `.streamlit/secrets.toml` as `DEEPSEEK_API_KEY`.

This feature is available below the chat bot in the main portfolio app:

```bash
streamlit run streamlit_app.py
```

You can also run just the checker:

```bash
streamlit run ats_tool.py
```
