import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/feedback.csv")

# Features and target
X = df["feedback"]
y = df["sentiment"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Test prediction
sample_feedback = [
    "The faculty is very supportive and teaches well"
]

sample_vector = vectorizer.transform(sample_feedback)
prediction = model.predict(sample_vector)

print("\nSample Feedback:")
print(sample_feedback[0])
print("Predicted Sentiment:", prediction[0])
# Save model and vectorizer
joblib.dump(model, "model/sentiment_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")