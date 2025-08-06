import streamlit as st
import json
from app.parser import extract_text_from_resume
from app.groq_client import call_groq_for_resume_structuring  # Your function that accepts the API key as argument

st.set_page_config(page_title="AI Resume Parser", page_icon="📄")
st.title("📄 AI Resume Parser")
st.markdown("Upload your **PDF** or **DOCX** resume to extract structured data using AI.")

# 🔑 User provides their Groq API key
groq_api_key = st.text_input("🔐 Enter your Groq API key", type="password")

uploaded_file = st.file_uploader("📁 Choose your resume file", type=["pdf", "docx"])

if uploaded_file and groq_api_key:
    st.info("Parsing and analyzing resume... please wait ⏳")

    # Detect content type
    content_type = uploaded_file.type

    # Extract text from resume
    extracted_text = extract_text_from_resume(uploaded_file, content_type)

    if not extracted_text:
        st.error("❌ Failed to extract text from the resume. Try another file.")
    else:
        # Send text to Groq API using user-provided key
        response_json = call_groq_for_resume_structuring(extracted_text, groq_api_key)

        if response_json:
            st.success("✅ Resume parsed successfully!")
            with st.expander("📋 Extracted Data (JSON)"):
                st.json(response_json)
        else:
            st.error("❌ AI model failed to extract data from resume.")
elif uploaded_file and not groq_api_key:
    st.warning("🔑 Please enter your Groq API key before uploading the resume.")
