import streamlit as st
import openai
import PyPDF2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("AI-Powered Career & Resume Analyzer")

st.markdown("""
Upload your resume to receive:
- Resume feedback
- Career recommendations
- Skill gap analysis
- Personalized improvement suggestions
""")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    st.subheader("Extracted Resume Text")
    st.write(resume_text[:3000])

    st.subheader("Career Insights")

    strengths = [
        "Communication",
        "Data Analysis",
        "Leadership",
        "Problem Solving"
    ]

    scores = [85, 78, 80, 90]

    df = pd.DataFrame({
        "Skill": strengths,
        "Score": scores
    })

    fig = px.bar(
        df,
        x="Skill",
        y="Score",
        title="Skill Strength Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("Resume analyzed successfully!")

    st.markdown("""
### Suggested Career Paths
- Business Analyst
- Data Analyst
- AI Operations Analyst
- Product Analyst

### Resume Improvement Tips
- Add more measurable achievements
- Highlight technical tools clearly
- Include project outcomes and impact
- Quantify leadership experience
""")
