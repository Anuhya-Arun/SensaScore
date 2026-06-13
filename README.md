# SensaScore - Headline Sensationalism Analyzer

SensaScore is an AI-powered system that analyzes news headlines for sensationalism on a scale from 0 to 4, where 0 represents completely factual and neutral content, and 4 represents extreme clickbait or highly misleading headlines.

## Features

- **Sensationalism Scoring**: Assigns scores from 0-4 based on sensationalism level
- **Multilingual Support**: Works with English and Hindi headlines
- **Explainable AI**: Provides reasons for the assigned score
- **Headline Rewriting**: Suggests neutral versions of sensational headlines
- **Batch Processing**: Analyze multiple headlines from CSV files
- **Web Interface**: User-friendly Streamlit dashboard
- **REST API**: Flask-based backend for integration

## Project Structure

```
sensascore/
├── backend/
│   └── app.py              # Flask REST API
├── frontend/
│   └── dashboard.py        # Streamlit web interface
├── model/
│   ├── train.py            # Model training script
│   ├── predict.py          # Prediction functions
│   ├── model.pkl           # Trained ML model
│   └── vectorizer.pkl      # TF-IDF vectorizer
├── utils/
│   ├── explain.py          # Rule-based explanation system
│   └── rewrite.py          # AI-powered headline rewriting
├── data/
│   └── final_dataset.csv   # Training dataset
├── requirements.txt        # Python dependencies
└── README.md
```

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the model (if needed):
   ```bash
   python model/train.py
   ```

## Usage

### Start the Backend API

```bash
python backend/app.py
```

The API will be available at `http://localhost:5000`

### Start the Web Interface

```bash
streamlit run frontend/dashboard.py
```

The dashboard will be available at `http://localhost:8501`

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/predict` - Single headline analysis
  ```json
  {
    "headline": "Unbelievable news shocks the world!"
  }
  ```
- `POST /api/batch_predict` - Batch analysis (multipart/form-data with CSV file)

## Score Interpretation

- **0-1**: Factual and neutral
- **1-2**: Slightly attention-grabbing
- **2-3**: Moderately sensational
- **3-4**: Highly sensational
- **4**: Extreme clickbait

## Technical Details

- **ML Model**: Linear Regression on TF-IDF features
- **Explanation**: Rule-based detection of sensational elements
- **Rewriting**: T5 transformer model for neutral headline generation
- **Backend**: Flask REST API
- **Frontend**: Streamlit web application

## Dataset

The system uses a custom multilingual dataset combining:
- English clickbait headlines with expanded scoring
- Hindi headlines with rule-based and synthetic scoring
- Balanced distribution across all score levels
