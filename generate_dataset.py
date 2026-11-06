import pandas as pd
import random

departments = ["IT", "CSE", "ECE", "EEE", "Mechanical"]

positive_starts = [
    "The faculty",
    "Teachers",
    "Laboratory facilities",
    "The curriculum",
    "Practical sessions",
    "The learning environment",
    "Course content",
    "Faculty members",
    "Infrastructure",
    "Classroom facilities"
]

positive_middle = [
    "are excellent",
    "are very helpful",
    "are well maintained",
    "are highly useful",
    "are well organized",
    "are very supportive",
    "are effective",
    "are informative",
    "are student friendly",
    "are impressive"
]

positive_end = [
    "for academic growth",
    "for skill development",
    "for practical learning",
    "for better understanding",
    "for career preparation",
    "for student success",
    "throughout the semester",
    "for overall development",
    "for project work",
    "for future opportunities"
]

negative_starts = [
    "The lab equipment",
    "Internet connectivity",
    "Classroom maintenance",
    "Practical sessions",
    "Infrastructure",
    "Course content",
    "Faculty interaction",
    "Computer systems",
    "Laboratories",
    "Technical resources"
]

negative_middle = [
    "is poor",
    "is outdated",
    "needs improvement",
    "is insufficient",
    "is disappointing",
    "is below expectations",
    "is slow",
    "requires upgrades",
    "is inadequate",
    "is limited"
]

negative_end = [
    "for effective learning",
    "for practical exposure",
    "during laboratory sessions",
    "for project development",
    "for student requirements",
    "throughout the semester",
    "in many situations",
    "for technical subjects",
    "for academic activities",
    "for overall performance"
]

neutral_starts = [
    "The curriculum",
    "Teaching quality",
    "Laboratories",
    "Infrastructure",
    "Faculty performance",
    "The course",
    "Practical sessions",
    "The learning environment",
    "Facilities",
    "Department resources"
]

neutral_middle = [
    "is average",
    "is satisfactory",
    "is acceptable",
    "is adequate",
    "is reasonable",
    "meets expectations",
    "is fairly good",
    "is moderate",
    "is standard",
    "is manageable"
]

neutral_end = [
    "for most students",
    "for academic needs",
    "for current requirements",
    "throughout the semester",
    "in general",
    "for regular coursework",
    "for day-to-day activities",
    "for learning purposes",
    "for department activities",
    "for educational requirements"
]

data = []

# Generate Positive
for _ in range(170):
    feedback = (
        random.choice(positive_starts)
        + " "
        + random.choice(positive_middle)
        + " "
        + random.choice(positive_end)
    )

    data.append([
        feedback,
        "Positive",
        random.choice(departments)
    ])

# Generate Negative
for _ in range(170):
    feedback = (
        random.choice(negative_starts)
        + " "
        + random.choice(negative_middle)
        + " "
        + random.choice(negative_end)
    )

    data.append([
        feedback,
        "Negative",
        random.choice(departments)
    ])

# Generate Neutral
for _ in range(160):
    feedback = (
        random.choice(neutral_starts)
        + " "
        + random.choice(neutral_middle)
        + " "
        + random.choice(neutral_end)
    )

    data.append([
        feedback,
        "Neutral",
        random.choice(departments)
    ])

random.shuffle(data)

df = pd.DataFrame(
    data,
    columns=["feedback", "sentiment", "department"]
)

df.to_csv(
    "data/generated_feedback.csv",
    index=False
)

print("Dataset generated successfully!")
print("Rows:", len(df))