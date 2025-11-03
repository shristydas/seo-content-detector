"""Content quality scoring utilities."""
import numpy as np
import pickle
from pathlib import Path
import os


def load_model(model_path=None):
    """Load the trained quality model."""
    try:
        # If no path provided, construct absolute path
        if model_path is None:
            # Get the directory of this file
            current_file = Path(__file__).resolve()
            # Go up to project root and find models directory
            project_root = current_file.parent.parent.parent
            model_path = project_root / 'models' / 'quality_model.pkl'

        # Convert to string for compatibility
        model_path = str(model_path)

        # Check if file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        return model_data['model'], model_data['feature_columns']
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")


def predict_quality(model, features, feature_columns):
    """
    Predict content quality.

    Args:
        model: Trained classifier
        features: Dict of features
        feature_columns: List of feature names

    Returns:
        Quality label (Low/Medium/High)
    """
    # Prepare features in correct order
    feature_array = np.array([[
        features[col] for col in feature_columns
    ]])

    # Predict
    prediction = model.predict(feature_array)[0]

    return prediction


def calculate_quality_score(features):
    """
    Calculate a 0-100 quality score based on features.

    Returns:
        int score 0-100
    """
    score = 0

    # Word count component (0-40 points)
    wc = features['word_count']
    if wc >= 1500:
        score += 40
    elif wc >= 1000:
        score += 30
    elif wc >= 500:
        score += 20
    else:
        score += 10

    # Readability component (0-40 points)
    readability = features['flesch_reading_ease']
    if 50 <= readability <= 70:
        score += 40
    elif 40 <= readability <= 80:
        score += 30
    elif readability > 0:
        score += 20
    else:
        score += 10

    # Sentence structure component (0-20 points)
    if features['sentence_count'] > 0:
        avg_words_per_sentence = features['word_count'] / features['sentence_count']
        if 15 <= avg_words_per_sentence <= 25:
            score += 20
        elif 10 <= avg_words_per_sentence <= 30:
            score += 15
        else:
            score += 10

    return min(score, 100)
