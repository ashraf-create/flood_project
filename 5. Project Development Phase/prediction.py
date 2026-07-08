import os
import joblib
import pandas as pd
import numpy as np

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'flood_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')

def load_model():
    """
    Loads the saved model and scaler.
    Raises FileNotFoundError if they are not yet trained and saved.
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            "Model files are missing. Please ensure 'dataset/flood.csv' is placed "
            "and run 'python train_model.py' to train and save the model."
        )
    
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def preprocess_input(input_data, scaler):
    """
    Validates and preprocesses input dictionary into scaled features.
    
    Parameters:
        input_data (dict): Dict containing user inputs for:
            - Annual_Rainfall
            - Monsoon_Intensity
            - Cloud_Coverage
            - Humidity
            - Temperature
            - River_Discharge
        scaler: The trained StandardScaler object.
        
    Returns:
        np.ndarray: 2D array of scaled features.
    """
    # Define expected columns matching the training schema exactly
    features_list = [
        'Annual_Rainfall',
        'Monsoon_Intensity',
        'Cloud_Coverage',
        'Humidity',
        'Temperature',
        'River_Discharge'
    ]
    
    # Extract values in the correct order
    raw_values = []
    for feature in features_list:
        val = input_data.get(feature)
        if val is None:
            raise ValueError(f"Missing required feature: {feature}")
        try:
            raw_values.append(float(val))
        except ValueError:
            raise ValueError(f"Invalid numeric value for {feature}: {val}")
            
    # Reshape for single-sample prediction: [[val1, val2, ...]]
    raw_array = np.array(raw_values).reshape(1, -1)
    
    # Scale the features
    scaled_array = scaler.transform(raw_array)
    return scaled_array

def predict_flood(input_data):
    """
    Performs full prediction pipeline on input dictionary.
    
    Parameters:
        input_data (dict): Unscaled user inputs.
        
    Returns:
        dict: Prediction results containing 'prediction' (0 or 1), 
              'probability' (float percentage), and 'status' (success/error).
    """
    try:
        model, scaler = load_model()
        scaled_features = preprocess_input(input_data, scaler)
        
        # Predict class (0 or 1)
        pred_class = int(model.predict(scaled_features)[0])
        
        # Predict probability if model supports it (all classification models here do)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(scaled_features)[0]
            # Probabilities: [prob_class_0, prob_class_1]
            flood_prob = float(probs[1]) * 100
        else:
            flood_prob = 100.0 if pred_class == 1 else 0.0
            
        return {
            'success': True,
            'prediction': pred_class,
            'probability': round(flood_prob, 2),
            'model_type': type(model).__name__
        }
        
    except FileNotFoundError as e:
        return {
            'success': False,
            'error_type': 'ModelNotTrained',
            'message': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error_type': 'PredictionError',
            'message': str(e)
        }
