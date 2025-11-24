import streamlit as st
import requests

st.set_page_config(page_title="Nirmaan AI Scoring Tool")
st.title("Nirmaan AI — Transcript Scoring Tool")

text = st.text_area("Paste transcript text:", height=250)
api = st.text_input("Backend URL:", "http://localhost:8000/score")

if st.button("Score Transcript"):
    if not text.strip():
        st.warning("Please enter a transcript.")
    else:
        with st.spinner("Scoring..."):
            r = requests.post(api, json={"text": text})
            data = r.json()

            st.header("Results")
            st.metric("Overall Score", data["overall_score"])
            st.write("Word Count:", data["word_count"])

            for c in data["criteria"]:
                st.subheader(c["name"])
                st.write("Score:", c["score"])
                st.write("Semantic Similarity:", c["semantic_similarity"])
                st.write("Keywords Found:", c["keywords_found"])
                st.write("Feedback:", c["feedback"])
