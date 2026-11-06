from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter
import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Student Dashboard", page_icon="👨‍🎓", layout="centered")

# Load model and vectorizer
model = joblib.load("model/sentiment_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

FEEDBACK_CSV = "data/feedback.csv"
DEPARTMENTS = ["IT", "CSE", "ECE", "EEE", "Mechanical"]

st.title("👨‍🎓 Student Dashboard")
st.markdown("Submit your feedback below. Your response is saved automatically.")
st.markdown("---")

department = st.selectbox("Select Your Department", DEPARTMENTS)
feedback = st.text_area("Enter Your Feedback", height=150, placeholder="Write your feedback here...")

if st.button("Analyze & Submit Feedback", use_container_width=True):
    if feedback.strip():
        # Predict sentiment
        feedback_vector = vectorizer.transform([feedback])
        prediction = model.predict(feedback_vector)[0]

        # Sentiment badge
        if prediction == "Positive":
            st.success(f"😊 Predicted Sentiment: **{prediction}**")
        elif prediction == "Negative":
            st.error(f"😞 Predicted Sentiment: **{prediction}**")
        else:
            st.info(f"😐 Predicted Sentiment: **{prediction}**")

        # Save to CSV
        new_row = pd.DataFrame({
            "feedback": [feedback],
            "sentiment": [prediction],
            "department": [department]
        })
        new_row.to_csv(FEEDBACK_CSV, mode="a", header=False, index=False)
        st.toast("✅ Feedback saved successfully!", icon="✅")

        # Feedback keywords
        st.subheader("🔑 Feedback Keywords")
        words = [w for w in feedback.lower().split() if w not in ENGLISH_STOP_WORDS and w.isalpha()]
        top_words = Counter(words).most_common(5)

        if top_words:
            cols = st.columns(len(top_words))
            for i, (word, _) in enumerate(top_words):
                cols[i].metric(label="", value=word)
        else:
            st.write("No significant keywords found.")
    else:
        st.warning("⚠️ Please enter your feedback before submitting.")
