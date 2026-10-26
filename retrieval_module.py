import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CSV_PATH = os.path.join("data", "emails.csv")

def load_emails():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame(columns=["email", "reply"])
    try:
        df = pd.read_csv(CSV_PATH).fillna("")
        if not {"email", "reply"}.issubset(df.columns):
            return pd.DataFrame(columns=["email", "reply"])
        return df
    except Exception:
        return pd.DataFrame(columns=["email", "reply"])

def find_similar_email(query, history):
    if history.empty:
        return None
    texts = history["email"].astype(str).tolist()
    if not any(t.strip() for t in texts):
        return None
    try:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(texts + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
        index = int(scores.argmax())
        if scores[index] <= 0:
            return None
        return {"email": texts[index], "reply": str(history.iloc[index]["reply"]),
                "score": float(scores[index])}
    except ValueError:
        return None
