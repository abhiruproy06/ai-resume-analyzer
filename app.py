import streamlit as st
from resume_parser import extract_resume_text
from matcher import analyze_resume

st.set_page_config(
page_title="AI Resume Analyzer",
page_icon="📄",
layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.subheader("Analyze your resume against a job description")

st.write(
"Upload your resume to discover relevant skills "
"and see how well it matches your target job."
)

resume = st.file_uploader(
"Upload your resume (PDF)",
type=["pdf"]
)

job_description = st.text_area(
"Paste the job description here",
height=250,
placeholder="Paste the complete job description..."
)

if st.button("Analyze Resume", type="primary"):

    if resume is None:
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Reading your resume..."):
                resume_text = extract_resume_text(resume)

            if not resume_text:
                st.warning(
                    "No readable text found. "
                    "This PDF may be scanned and require OCR."
                )

            else:
                st.success("Resume text extracted successfully!")

                st.subheader("Extracted Resume Text")

                st.text_area(
                    "Resume content",
                    value=resume_text,
                    height=300
                )

                st.caption(
                    f"Characters extracted: {len(resume_text)}"
                )
                st.divider()
                st.subheader("🎯 Resume–Job Match Analysis")

                try:
                    results = analyze_resume(
                        resume_text,
                        job_description
                    )

                    col1, col2 = st.columns(2)
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Text Similarity",
                            f"{results['similarity_score']}%"
                        )

                    with col2:
                        coverage = results["skill_coverage"]

                        st.metric(
                            "Required Skill Coverage",
                            f"{coverage}%"
                            if coverage is not None
                            else "Not available"
                        )
                    with col3:
                        st.metric(
                          "Semantic Similarity",
                         f"{results['semantic_score']}%"
    )

                    st.caption(
                        "Text similarity measures wording overlap. "
                        "Skill coverage measures detected job skills "
                        "also mentioned in the resume. Neither score "
                        "predicts hiring probability."
                    )

                    st.subheader("✅ Matched Skills")

                    if results["matched_skills"]:
                        st.write(", ".join(results["matched_skills"]))
                    else:
                        st.info("No matching skills detected.")

                    st.subheader("📚 Skills Not Detected in Resume")

                    if results["missing_skills"]:
                        st.write(", ".join(results["missing_skills"]))
                    elif results["job_skills"]:
                        st.success("All detected job skills were found.")
                    else:
                        st.info("No recognized skills found in the job description.")

                except ValueError as error:
                    st.error(str(error))
                

        except ValueError as error:
            st.error(str(error))

