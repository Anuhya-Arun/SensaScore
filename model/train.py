import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import joblib
import os
import numpy as np

# get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# build correct path to dataset
data_path = os.path.join(BASE_DIR, "..", "data", "final_dataset.csv")

print("Loading dataset from:", data_path)

# load dataset
df = pd.read_csv(data_path, encoding="utf-8")

print(df.head())

# Feature engineering
df['length'] = df['headline'].apply(len)
df['exclamation_count'] = df['headline'].apply(lambda x: x.count('!'))
df['question_count'] = df['headline'].apply(lambda x: x.count('?'))
df['caps_ratio'] = df['headline'].apply(lambda x: sum(1 for c in x if c.isupper()) / len(x) if len(x) > 0 else 0)

# split data
X_text = df["headline"]
X_features = df[['length', 'exclamation_count', 'question_count', 'caps_ratio']]
y = df["score"]

# vectorize text
vectorizer = TfidfVectorizer(max_features=5000)
X_text_vec = vectorizer.fit_transform(X_text)

# combine features
from scipy.sparse import hstack
X_combined = hstack([X_text_vec, X_features.values])

# train model
model = LinearRegression()
model.fit(X_combined, y)

# save model in same folder
model_path = os.path.join(BASE_DIR, "model.pkl")
vec_path = os.path.join(BASE_DIR, "vectorizer.pkl")

joblib.dump(model, model_path)
joblib.dump(vectorizer, vec_path)

print("✅ Model trained and saved with additional features!")