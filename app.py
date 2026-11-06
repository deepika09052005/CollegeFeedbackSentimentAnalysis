import streamlit as st

st.set_page_config(
    page_title="College Feedback Sentiment Analysis",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 College Feedback Sentiment Analysis")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👨‍🎓 Student Dashboard")
    st.write("Submit your feedback and get instant sentiment analysis.")
    if st.button("Go to Student Dashboard", use_container_width=True):
        st.switch_page("pages/student.py")

with col2:
    st.subheader("🏫 Management Dashboard")
    st.write("View analytics, sentiment trends, and department insights.")
    if st.button("Go to Management Dashboard", use_container_width=True):
        st.switch_page("pages/management.py")

st.markdown("---")
st.caption("Use the sidebar to navigate between dashboards.")
