import pandas as pd
import sys
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.predict import predict_score

# Load dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'final_dataset.csv'))

print("\n" + "="*60)
print("MODEL EVALUATION - SENSASCORE")
print("="*60)

# Get predictions
y_true = df['score'].values
y_pred = []

print("\nGenerating predictions...")
for i, headline in enumerate(df['headline']):
    try:
        pred = predict_score(headline)
        y_pred.append(pred)
    except Exception as e:
        print(f"Error predicting headline {i}: {e}")
        y_pred.append(2.0)  # default to middle score

y_pred = np.array(y_pred)

# Calculate metrics
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print("\n" + "="*60)
print("OVERALL METRICS")
print("="*60)
print(f"Total Samples: {len(df)}")
print(f"Score Range: 0-4 (continuous)")
print(f"\nMean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# Per-score analysis
print("\n" + "="*60)
print("ERROR ANALYSIS BY SCORE LEVEL")
print("="*60)
for score in range(5):
    mask = y_true == score
    if mask.sum() > 0:
        score_mae = mean_absolute_error(y_true[mask], y_pred[mask])
        print(f"Score {score}: {mask.sum()} samples | MAE: {score_mae:.4f}")

# Show sample predictions
print("\n" + "="*60)
print("SAMPLE PREDICTIONS (Random 15 samples)")
print("="*60)

sample_indices = np.random.choice(len(df), min(15, len(df)), replace=False)
for idx in sample_indices:
    headline = df['headline'].iloc[idx][:50]
    true_score = y_true[idx]
    pred_score = y_pred[idx]
    error = abs(true_score - pred_score)
    print(f"\nHeadline: {headline}...")
    print(f"  True: {true_score:.1f} | Pred: {pred_score:.2f} | Error: {error:.2f}")

print("\n" + "="*60)
print("✅ MODEL EVALUATION COMPLETE")
print("="*60 + "\n")
