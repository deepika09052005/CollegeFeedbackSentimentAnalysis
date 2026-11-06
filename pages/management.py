from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st
import pandas as pd
import joblib

matplotlib.use("Agg")

st.set_page_config(page_title="Management Dashboard", page_icon="🏫", layout="wide")

FEEDBACK_CSV = "data/feedback.csv"
DEPARTMENTS = ["IT", "CSE", "ECE", "EEE", "Mechanical"]

st.title("🏫 Management Dashboard")
st.markdown("Analytics and insights across all departments.")
st.markdown("---")


@st.cache_data(ttl=30)
def load_data():
    return pd.read_csv(FEEDBACK_CSV)


def get_sentiment_counts(data):
    positive = len(data[data["sentiment"] == "Positive"])
    negative = len(data[data["sentiment"] == "Negative"])
    neutral = len(data[data["sentiment"] == "Neutral"])
    return positive, negative, neutral


def satisfaction_score(positive, total):
    return (positive / total * 100) if total > 0 else 0


def top_keywords(text, n=5):
    words = [w for w in text.lower().split() if w not in ENGLISH_STOP_WORDS and w.isalpha()]
    return Counter(words).most_common(n)


def improvement_suggestions(negative_text):
    checks = {
        "lab": "Upgrade laboratory facilities and equipment.",
        "practical": "Increase hands-on practical sessions.",
        "infrastructure": "Improve campus infrastructure and maintenance.",
        "slow": "Upgrade computer systems and network resources.",
        "classroom": "Improve classroom maintenance and learning environment.",
        "internet": "Improve internet connectivity across campus.",
        "outdated": "Replace outdated equipment and course materials.",
    }
    suggestions = [msg for kw, msg in checks.items() if kw in negative_text.lower()]
    return suggestions or ["No major issues detected. Continue maintaining quality standards."]


# ── Sidebar: department filter ──────────────────────────────────────────────
st.sidebar.header("Filter")
selected_dept = st.sidebar.selectbox("Select Department", ["All"] + DEPARTMENTS)
st.sidebar.markdown("---")
st.sidebar.caption("Data refreshes every 30 seconds.")

df = load_data()

dept_df = df if selected_dept == "All" else df[df["department"] == selected_dept]
dept_label = selected_dept if selected_dept != "All" else "All Departments"

# ── KPI row ──────────────────────────────────────────────────────────────────
pos, neg, neu = get_sentiment_counts(dept_df)
total = len(dept_df)
score = satisfaction_score(pos, total)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📋 Total Feedback", total)
k2.metric("😊 Positive", pos)
k3.metric("😞 Negative", neg)
k4.metric("😐 Neutral", neu)
k5.metric("⭐ Satisfaction Score", f"{score:.1f}%")

st.markdown("---")

# ── Charts row ───────────────────────────────────────────────────────────────
st.subheader(f"📊 Sentiment Distribution — {dept_label}")

chart_col1, chart_col2 = st.columns(2)

sentiment_counts = {"Positive": pos, "Negative": neg, "Neutral": neu}
colors = {"Positive": "#4CAF50", "Negative": "#F44336", "Neutral": "#2196F3"}

with chart_col1:
    st.markdown("**Bar Chart**")
    fig_bar, ax_bar = plt.subplots(figsize=(5, 3))
    ax_bar.bar(
        sentiment_counts.keys(),
        sentiment_counts.values(),
        color=[colors[k] for k in sentiment_counts],
        edgecolor="white",
        width=0.5
    )
    ax_bar.set_ylabel("Count")
    ax_bar.set_title("Sentiment Distribution")
    ax_bar.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig_bar)
    plt.close(fig_bar)

with chart_col2:
    st.markdown("**Pie Chart**")
    non_zero = {k: v for k, v in sentiment_counts.items() if v > 0}
    if non_zero:
        fig_pie, ax_pie = plt.subplots(figsize=(5, 3))
        ax_pie.pie(
            non_zero.values(),
            labels=non_zero.keys(),
            colors=[colors[k] for k in non_zero],
            autopct="%1.1f%%",
            startangle=140
        )
        ax_pie.set_title("Sentiment Share")
        st.pyplot(fig_pie)
        plt.close(fig_pie)
    else:
        st.info("No data available for pie chart.")

st.markdown("---")

# ── Department Comparison Chart ───────────────────────────────────────────────
st.subheader("🏆 Department Comparison — Satisfaction Scores")

dept_scores = []
for dept in DEPARTMENTS:
    d = df[df["department"] == dept]
    p = len(d[d["sentiment"] == "Positive"])
    dept_scores.append({"Department": dept, "Satisfaction (%)": satisfaction_score(p, len(d))})

dept_score_df = pd.DataFrame(dept_scores).sort_values("Satisfaction (%)", ascending=False)

fig_comp, ax_comp = plt.subplots(figsize=(8, 3.5))
bar_colors = ["#4CAF50" if s >= 60 else "#FF9800" if s >= 40 else "#F44336"
              for s in dept_score_df["Satisfaction (%)"]]
ax_comp.barh(dept_score_df["Department"], dept_score_df["Satisfaction (%)"],
             color=bar_colors, edgecolor="white")
ax_comp.set_xlabel("Satisfaction Score (%)")
ax_comp.set_title("Satisfaction Score by Department")
ax_comp.set_xlim(0, 100)
ax_comp.spines[["top", "right"]].set_visible(False)
for i, (val, dept) in enumerate(zip(dept_score_df["Satisfaction (%)"], dept_score_df["Department"])):
    ax_comp.text(val + 1, i, f"{val:.1f}%", va="center", fontsize=9)
st.pyplot(fig_comp)
plt.close(fig_comp)

st.markdown("---")

# ── Word Cloud ────────────────────────────────────────────────────────────────
st.subheader(f"☁️ Word Cloud — {dept_label}")

if total > 0:
    all_text = " ".join(dept_df["feedback"].dropna())
    wc = WordCloud(
        width=900, height=350,
        background_color="white",
        stopwords=set(ENGLISH_STOP_WORDS),
        colormap="viridis"
    ).generate(all_text)
    fig_wc, ax_wc = plt.subplots(figsize=(9, 3.5))
    ax_wc.imshow(wc, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
    plt.close(fig_wc)
else:
    st.info("No feedback data available to generate word cloud.")

st.markdown("---")

# ── Top Keywords ──────────────────────────────────────────────────────────────
st.subheader(f"🔑 Top Keywords — {dept_label}")

pos_text = " ".join(dept_df[dept_df["sentiment"] == "Positive"]["feedback"].dropna())
neg_text = " ".join(dept_df[dept_df["sentiment"] == "Negative"]["feedback"].dropna())

kw_col1, kw_col2 = st.columns(2)

with kw_col1:
    st.success("✅ Top Positive Keywords")
    for word, count in top_keywords(pos_text):
        st.write(f"✅ {word} ({count})")

with kw_col2:
    st.error("❌ Top Negative Keywords")
    for word, count in top_keywords(neg_text):
        st.write(f"❌ {word} ({count})")

st.markdown("---")

# ── Improvement Suggestions ───────────────────────────────────────────────────
st.subheader(f"💡 Improvement Suggestions — {dept_label}")
for suggestion in improvement_suggestions(neg_text):
    st.write("•", suggestion)

st.markdown("---")

# ── All Feedback Table ────────────────────────────────────────────────────────
st.subheader(f"📄 All Submitted Feedback — {dept_label}")

if total > 0:
    display_df = dept_df[["department", "sentiment", "feedback"]].reset_index(drop=True)
    display_df.index += 1

    def highlight_sentiment(val):
        color_map = {"Positive": "#d4edda", "Negative": "#f8d7da", "Neutral": "#d1ecf1"}
        return f"background-color: {color_map.get(val, '')}"

    try:
        styled = display_df.style.map(highlight_sentiment, subset=["sentiment"])
    except AttributeError:
        styled = display_df.style.applymap(highlight_sentiment, subset=["sentiment"])

    st.dataframe(styled, use_container_width=True, height=400)
else:
    st.info("No feedback records found for the selected department.")
