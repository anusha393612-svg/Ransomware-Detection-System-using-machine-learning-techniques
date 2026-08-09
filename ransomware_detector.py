#!/usr/bin/env python3
"""
Ransomware Detection ML Backend
Uses PE header features to classify executables as Ransomware or Benign.
"""

import json
import sys
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import hashlib

# PE Header Features we'll extract and use
FEATURE_NAMES = [
    'entropy',
    'num_sections',
    'num_imports',
    'num_exports',
    'has_debug_info',
    'has_relocation_info',
    'virtual_size',
    'raw_size',
    'num_resources',
    'is_dll',
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')


def generate_synthetic_dataset(n_samples=1000):
    """
    Generate synthetic PE header features for training.
    In production, this would use real PE files from VirusTotal or similar.
    """
    np.random.seed(42)
    X = []
    y = []
    
    # Generate benign samples (typically have lower entropy, more imports, etc.)
    for _ in range(n_samples // 2):
        features = [
            np.random.uniform(3.5, 6.5),      # entropy: lower for benign
            np.random.randint(2, 8),          # num_sections
            np.random.randint(5, 50),         # num_imports: higher for benign
            np.random.randint(0, 10),         # num_exports
            np.random.choice([0, 1]),         # has_debug_info
            np.random.choice([0, 1]),         # has_relocation_info
            np.random.randint(1000, 100000),  # virtual_size
            np.random.randint(1000, 100000),  # raw_size
            np.random.randint(0, 100),        # num_resources
            np.random.choice([0, 1]),         # is_dll
        ]
        X.append(features)
        y.append(0)  # Benign
    
    # Generate ransomware samples (typically have higher entropy, fewer imports, etc.)
    for _ in range(n_samples // 2):
        features = [
            np.random.uniform(7.0, 7.99),     # entropy: higher for ransomware
            np.random.randint(3, 12),         # num_sections
            np.random.randint(0, 20),         # num_imports: lower for ransomware
            np.random.randint(0, 5),          # num_exports
            np.random.choice([0, 1]),         # has_debug_info
            np.random.choice([0, 1]),         # has_relocation_info
            np.random.randint(10000, 500000), # virtual_size: larger for ransomware
            np.random.randint(10000, 500000), # raw_size: larger for ransomware
            np.random.randint(0, 50),         # num_resources
            np.random.choice([0, 1]),         # is_dll
        ]
        X.append(features)
        y.append(1)  # Ransomware
    
    return np.array(X), np.array(y)


def train_model():
    """Train the Random Forest model on synthetic PE header data."""
    print("Generating synthetic training data...", file=sys.stderr)
    X, y = generate_synthetic_dataset(n_samples=2000)
    
    print("Training Random Forest model...", file=sys.stderr)
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)
    
    # Train scaler for feature normalization
    scaler = StandardScaler()
    scaler.fit(X)
    
    # Save model and scaler
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"Model saved to {MODEL_PATH}", file=sys.stderr)
    print(f"Scaler saved to {SCALER_PATH}", file=sys.stderr)
    
    return model, scaler


def load_model():
    """Load the trained model and scaler from disk."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("Model not found. Training new model...", file=sys.stderr)
        return train_model()
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler


def predict(features_dict):
    """
    Predict ransomware classification for given PE header features.
    
    Args:
        features_dict: Dictionary with keys matching FEATURE_NAMES
    
    Returns:
        Dictionary with prediction, confidence, and feature importance
    """
    model, scaler = load_model()
    
    # Extract features in the correct order
    features = []
    for feature_name in FEATURE_NAMES:
        if feature_name in features_dict:
            features.append(float(features_dict[feature_name]))
        else:
            # Use default value if feature is missing
            features.append(0.0)
    
    features = np.array([features])
    
    # Get prediction and confidence
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Confidence is the probability of the predicted class
    confidence = int(probabilities[prediction] * 100)
    
    # Get feature importance
    feature_importance = dict(zip(FEATURE_NAMES, model.feature_importances_))
    
    # Sort by importance
    sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    top_features = sorted_importance[:5]  # Top 5 most important features
    
    result = {
        'prediction': 'Ransomware' if prediction == 1 else 'Benign',
        'confidence': confidence,
        'probability_benign': int(probabilities[0] * 100),
        'probability_ransomware': int(probabilities[1] * 100),
        'top_features': [{'name': name, 'importance': float(imp)} for name, imp in top_features],
    }
    
    return result


def main():
    """Main entry point for the ML backend."""
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No action specified'}))
        sys.exit(1)
    
    action = sys.argv[1]
    
    try:
        if action == 'train':
            train_model()
            print(json.dumps({'status': 'Model trained successfully'}))
        
        elif action == 'predict':
            if len(sys.argv) < 3:
                print(json.dumps({'error': 'No features provided'}))
                sys.exit(1)
            
            features_json = sys.argv[2]
            features_dict = json.loads(features_json)
            result = predict(features_dict)
            print(json.dumps(result))
        
        else:
            print(json.dumps({'error': f'Unknown action: {action}'}))
            sys.exit(1)
    
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
