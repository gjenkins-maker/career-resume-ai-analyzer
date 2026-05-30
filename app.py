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

# ---------- Helper Functions ----------

def clean_resume_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def format_keyword(keyword):
    special_cases = {
        "sql": "SQL",
        "ai": "AI",
        "openai": "OpenAI",
        "github": "GitHub",
        "excel": "Excel",
        "python": "Python",
        "streamlit": "Streamlit",
        "plotly": "Plotly",
        "business analytics": "Business Analytics",
        "data analysis": "Data Analysis",
        "data visualization": "Data Visualization",
        "dashboard": "Dashboard",
        "machine learning": "Machine Learning",
        "artificial intelligence": "Artificial Intelligence",
        "prompt engineering": "Prompt Engineering",
        "project": "Project",
        "analytics": "Analytics"
    }

    return special_cases.get(keyword.lower(), keyword.title())


def calculate_resume_score(text):
    keywords = [
        "python", "sql", "data analysis", "data visualization", "dashboard",
        "streamlit", "plotly", "machine learning", "artificial intelligence",
        "ai", "github", "excel", "business analytics", "project", "analytics",
        "openai", "prompt engineering"
    ]

    text_lower = text.lower()
    matched = [word for word in keywords if word in text_lower]
    missing = [word for word in keywords if word not in text_lower]

    base_score = int((len(matched) / len(keywords)) * 75) + 15
    score = min(base_score, 94)

    return score, matched, missing


def career_match_scores(text):
    text_lower = text.lower()

    careers = {
        "Business Analyst": {
            "keywords": ["business analytics", "excel", "strategy", "dashboard", "data analysis", "analytics"],
            "base": 18
        },
        "Data Analyst": {
            "keywords": ["python", "sql", "data visualization", "plotly", "analytics", "data analysis"],
            "base": 15
        },
        "AI Operations Analyst": {
            "keywords": ["artificial intelligence", "ai", "openai", "machine learning", "prompt engineering"],
            "base": 12
        },
        "Product Analyst": {
            "keywords": ["user", "dashboard", "insights", "business", "data", "project"],
            "base": 10
        }
    }

    results = []

    for career, data in careers.items():
        keywords = data["keywords"]
        match_count = sum(1 for keyword in keywords if keyword in text_lower)

        raw_score = int((match_count / len(keywords)) * 80) + data["base"]
        score = min(raw_score, 96)

        results.append({
            "Career Path": career,
            "Match Score": score
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Match Score", ascending=False)

    return df


def generate_strengths(matched_keywords):
    strengths = []

    if "python" in matched_keywords:
        strengths.append("Strong Python foundation shown through technical projects.")
    if "streamlit" in matched_keywords or "dashboard" in matched_keywords:
        strengths.append("Experience building interactive dashboards and web applications.")
    if "data analysis" in matched_keywords or "analytics" in matched_keywords:
        strengths.append("Clear alignment with analytics and data-driven decision-making roles.")
    if "artificial intelligence" in matched_keywords or "ai" in matched_keywords or "openai" in matched_keywords:
        strengths.append("Relevant exposure to AI applications and emerging technologies.")
    if "github" in matched_keywords:
        strengths.append("Project work is supported by GitHub, which strengthens portfolio credibility.")

    if not strengths:
        strengths.append("Resume shows potential, but more technical keywords would make it stronger.")

    return strengths


def generate_improvements(missing_keywords):
    improvements = [
        "Add more measurable outcomes, such as percentages, project impact, or performance improvements.",
        "Tailor resume keywords to each job description before applying.",
        "Use strong action verbs such as developed, built, analyzed, evaluated, and deployed."
    ]

    if "sql" in missing_keywords:
        improvements.append("Add SQL experience if relevant, since many analyst roles require it.")
    if "excel" in missing_keywords:
        improvements.append("Mention Excel if you have used it for business or analytics coursework.")
    if "data visualization" in missing_keywords:
        improvements.append("Highlight data visualization experience more clearly.")
    if "machine learning" in missing_keywords:
        improvements.append("Add machine learning coursework or project experience if applicable.")

    return improvements


def overall_recommendation(career_df):
    top_role = career_df.iloc[0]["Career Path"]
    top_score = career_df.iloc[0]["Match Score"]

    return (
        f"This resume is strongest for **{top_role}** roles with a **{top_score}% match**. "
        f"The profile shows a strong combination of analytics, technical project work, and business-focused problem solving. "
        f"To make the resume even stronger, the candidate should continue adding measurable outcomes, clearer project impact, "
        f"and role-specific keywords for each application."
    )


def score_summary(score):
    if score >= 90:
        return "Strong resume for analytics-focused roles."
    elif score >= 80:
        return "Good resume with room for stronger measurable impact."
    elif score >= 70:
        return "Solid foundation, but more technical keywords and project outcomes would help."
    else:
        return "Resume needs stronger role-specific keywords and clearer project impact."


# ---------- App Layout ----------

st.title("AI-Powered Career & Resume Analyzer")
st.caption(
    "Upload a resume to receive resume scoring, career match insights, skill analysis, "
    "and personalized improvement recommendations."
)

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
    strengths = generate_strengths(matched_keywords)
    improvements = generate_improvements(missing_keywords)
    recommendation = overall_recommendation(career_df)
    summary = score_summary(score)

    st.success("Resume uploaded and analyzed successfully!")

    # ---------- Resume Overview ----------

    st.markdown("## Resume Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Resume Score", f"{score}/100")
        st.caption(summary)

    with col2:
        st.metric("Keywords Found", len(matched_keywords))
        st.caption("Relevant ATS and analytics keywords detected.")

    with col3:
        best_match = career_df.iloc[0]["Career Path"]
        st.metric("Best Career Match", best_match)
        st.caption("Based on resume keywords and project experience.")

    st.markdown("---")

    # ---------- Overall Recommendation ----------

    st.markdown("## Overall Recommendation")
    st.info(recommendation)

    st.markdown("---")

    # ---------- Career Match Chart ----------

    st.markdown("## Career Match Analysis")

    fig_career = px.bar(
        career_df,
        x="Career Path",
        y="Match Score",
        title="Career Match Score by Role",
        text="Match Score"
    )

    fig_career.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_career.update_layout(
        yaxis_range=[0, 100],
        xaxis_title="Career Path",
        yaxis_title="Match Score"
    )

    st.plotly_chart(fig_career, use_container_width=True)

    st.markdown("---")

    # ---------- Skill and Keyword Analysis ----------

    st.markdown("## Skill & Keyword Analysis")

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Detected Strengths")
        for strength in strengths:
            st.write(f"✅ {strength}")

    with col5:
        st.subheader("Recommended Improvements")
        for improvement in improvements:
            st.write(f"➕ {improvement}")

    st.markdown("---")

    # ---------- Suggested Career Paths ----------

    st.markdown("## Suggested Career Paths")

    for _, row in career_df.iterrows():
        st.write(f"**{row['Career Path']}** — {row['Match Score']}% match")

    st.markdown("---")

    # ---------- ATS Keyword Scan ----------

    st.markdown("## ATS Keyword Scan")

    col6, col7 = st.columns(2)

    with col6:
        st.subheader("Keywords Found")
        if matched_keywords:
            for keyword in matched_keywords:
                st.write(f"✅ {format_keyword(keyword)}")
        else:
            st.write("No major keywords detected.")

    with col7:
        st.subheader("Suggested Keywords to Add")
        if missing_keywords:
            for keyword in missing_keywords[:8]:
                st.write(f"➕ {format_keyword(keyword)}")
        else:
            st.write("Your resume includes most key keywords.")

    st.markdown("---")

    # ---------- Extracted Text Hidden in Expander ----------

    with st.expander("View Extracted Resume Text"):
        st.text_area("Resume Text Preview", resume_text[:3000], height=180)

    st.markdown("---")

    # ---------- Downloadable Report ----------

    report = f"""
AI Career & Resume Analyzer Report

Resume Score: {score}/100
Resume Summary: {summary}

Best Career Match:
{career_df.iloc[0]["Career Path"]} - {career_df.iloc[0]["Match Score"]}% match

Career Match Scores:
{career_df.to_string(index=False)}

Detected Keywords:
{", ".join([format_keyword(keyword) for keyword in matched_keywords])}

Suggested Keywords to Add:
{", ".join([format_keyword(keyword) for keyword in missing_keywords[:10]])}

Top Strengths:
{chr(10).join(["- " + strength for strength in strengths])}

Recommended Improvements:
{chr(10).join(["- " + improvement for improvement in improvements])}

Overall Recommendation:
{recommendation}
"""

    st.download_button(
        label="Download Resume Feedback Report",
        data=report,
        file_name="resume_feedback_report.txt",
        mime="text/plain"
    )

else:
    st.info("Upload a PDF resume to begin the analysis.")
