import joblib
import os
import sys
import numpy as np

# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.explain import explain
# Lazy import for rewrite to avoid slow loading
# from utils.rewrite import rewrite

# get path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vec_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# load model
model = joblib.load(model_path)
vectorizer = joblib.load(vec_path)

def predict_score(text):
    # Feature engineering
    length = len(text)
    exclamation_count = text.count('!')
    question_count = text.count('?')
    caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    
    # vectorize text
    text_vec = vectorizer.transform([text])
    
    # combine
    from scipy.sparse import hstack
    features = np.array([[length, exclamation_count, question_count, caps_ratio]])
    combined = hstack([text_vec, features])
    
    score = model.predict(combined)[0]
    # Clamp score between 0 and 4
    score = max(0, min(4, score))
    return round(score, 2)

def get_rewrite(text):
    # Lazy import to avoid loading T5 model on startup
    from utils.rewrite import rewrite
    return rewrite(text)

# test
if __name__ == "__main__":
    while True:
        text = input("Enter headline: ")
        print("Score:", predict_score(text))
        print("Explanation:", explain(text))
        print("Rewritten:", get_rewrite(text))