import streamlit as st
import PyPDF2
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    page_title="AI Career & Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

def clean_resume_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_resume_score(text):
    keywords = [
        "python", "sql", "data analysis", "data visualization", "dashboard",
        "streamlit", "plotly", "machine learning", "artificial intelligence",
        "ai", "github", "excel", "business analytics", "project", "analytics"
    ]

    text_lower = text.lower()
    matched = [word for word in keywords if word in text_lower]
    score = min(100, int((len(matched) / len(keywords)) * 100) + 25)

    return score, matched, [word for word in keywords if word not in text_lower]

def career_match_scores(text):
    text_lower = text.lower()

    careers = {
        "Business Analyst": ["business analytics", "excel", "strategy", "dashboard", "data analysis"],
        "Data Analyst": ["python", "sql", "data visualization", "plotly", "analytics"],
        "AI Operations Analyst": ["artificial intelligence", "ai", "openai", "machine learning", "prompt engineering"],
        "Product Analyst": ["user", "dashboard", "insights", "business", "data"]
    }

    results = []

    for career, keywords in careers.items():
        match_count = sum(1 for keyword in keywords if keyword in text_lower)
        score = int((match_count / len(keywords)) * 100)
        results.append({"Career Path": career, "Match Score": score})

    return pd.DataFrame(results)

st.title("AI-Powered Career & Resume Analyzer")
st.caption("Upload a resume to receive career insights, resume scoring, skill analysis, and personalized improvement suggestions.")

st.markdown("---")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text + " "

    resume_text = clean_resume_text(resume_text)

    score, matched_keywords, missing_keywords = calculate_resume_score(resume_text)
    career_df = career_match_scores(resume_text)

    st.success("Resume uploaded and analyzed successfully!")

    st.markdown("## Resume Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resume Score", f"{score}/100")

    with col2:
        st.metric("Keywords Found", len(matched_keywords))

    with col3:
        st.metric("Career Matches", "4")

    st.markdown("---")

    st.markdown("## Extracted Resume Text")
    st.text_area("Resume Text Preview", resume_text[:3000], height=220)

    st.markdown("---")

    st.markdown("## Career Match Analysis")

    fig_career = px.bar(
        career_df,
        x="Career Path",
        y="Match Score",
        title="Career Match Score by Role",
        text="Match Score"
    )

    fig_career.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_career.update_layout(yaxis_range=[0, 100])

    st.plotly_chart(fig_career, use_container_width=True)

    st.markdown("---")

    st.markdown("## Skill & Keyword Analysis")

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Detected Strengths")
        if matched_keywords:
            for keyword in matched_keywords:
                st.write(f"✅ {keyword.title()}")
        else:
            st.write("No strong keywords detected yet.")

    with col5:
        st.subheader("Recommended Skills to Add")
        if missing_keywords:
            for keyword in missing_keywords[:8]:
                st.write(f"➕ {keyword.title()}")
        else:
            st.write("Your resume includes most key skills.")

    st.markdown("---")

    st.markdown("## Suggested Career Paths")

    top_careers = career_df.sort_values(by="Match Score", ascending=False)

    for _, row in top_careers.iterrows():
        st.write(f"**{row['Career Path']}** — {row['Match Score']}% match")

    st.markdown("---")

    st.markdown("## Resume Improvement Recommendations")

    tips = [
        "Add more measurable achievements, such as percentages, project outcomes, or impact.",
        "Highlight technical tools clearly in the skills and project sections.",
        "Include links to GitHub repositories and deployed applications when possible.",
        "Use action verbs such as developed, built, analyzed, evaluated, and deployed.",
        "Tailor your resume keywords to the specific job description before applying."
    ]

    for tip in tips:
        st.write(f"• {tip}")

    st.markdown("---")

    report = f"""
AI Career & Resume Analyzer Report

Resume Score: {score}/100

Detected Keywords:
{", ".join(matched_keywords)}

Recommended Skills to Add:
{", ".join(missing_keywords[:10])}

Top Career Matches:
{career_df.to_string(index=False)}

Resume Improvement Tips:
- Add measurable achievements.
- Highlight technical tools clearly.
- Include GitHub and live project links.
- Use stronger action verbs.
- Tailor resume keywords to each job description.
"""

    st.download_button(
        label="Download Resume Feedback Report",
        data=report,
        file_name="resume_feedback_report.txt",
        mime="text/plain"
    )

else:
    st.info("Upload a PDF resume to begin the analysis.")
