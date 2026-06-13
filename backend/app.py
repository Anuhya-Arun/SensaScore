from flask import Flask, request, jsonify
import pandas as pd
import os
import sys
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.predict import predict_score, get_rewrite
from utils.explain import explain

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'SensaScore API is running'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'headline' not in data:
        return jsonify({'error': 'Missing headline'}), 400

    headline = data['headline']
    score = predict_score(headline)
    explanation = explain(headline)
    rewritten = get_rewrite(headline)

    return jsonify({
        'headline': headline,
        'score': score,
        'explanation': explanation,
        'rewritten': get_rewrite(headline)
    })

@app.route('/api/batch_predict', methods=['POST'])
def batch_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV'}), 400

    try:
        df = pd.read_csv(file, encoding='utf-8')
        if 'headline' not in df.columns:
            return jsonify({'error': 'CSV must have a "headline" column'}), 400

        results = []
        scores = []

        for _, row in df.iterrows():
            headline = str(row['headline'])
            score = predict_score(headline)
            explanation = explain(headline)
            rewritten = get_rewrite(headline)

            results.append({
                'headline': headline,
                'score': score,
                'explanation': explanation,
                'rewritten': get_rewrite(headline)
            })
            scores.append(score)

        # Summary statistics
        summary = {
            'total_headlines': len(results),
            'average_score': round(sum(scores) / len(scores), 2),
            'score_distribution': {
                '0-1': sum(1 for s in scores if s < 1),
                '1-2': sum(1 for s in scores if 1 <= s < 2),
                '2-3': sum(1 for s in scores if 2 <= s < 3),
                '3-4': sum(1 for s in scores if 3 <= s < 4),
                '4': sum(1 for s in scores if s == 4)
            }
        }

        return jsonify({
            'summary': summary,
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['GET'])
def evaluate():
    """Evaluate model accuracy on the dataset"""
    try:
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        import numpy as np
        
        df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'final_dataset.csv'))
        
        y_true = df['score'].values
        y_pred = []
        
        for headline in df['headline']:
            try:
                pred = predict_score(headline)
                y_pred.append(pred)
            except:
                y_pred.append(2.0)
        
        y_pred = np.array(y_pred)
        
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        return jsonify({
            'total_samples': len(df),
            'mean_absolute_error': round(mae, 4),
            'rmse': round(rmse, 4),
            'r2_score': round(r2, 4),
            'accuracy_percentage': round((1 - (mae / 2)) * 100, 2),  # Assuming scale 0-4, max error is 2
            'message': f'Model provides predictions with ~{round((1 - (mae / 2)) * 100, 1)}% accuracy'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Could not evaluate model'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)