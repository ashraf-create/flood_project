import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file

from prediction import predict_flood, MODEL_PATH, SCALER_PATH

app = Flask(__name__)
app.secret_key = 'rising_waters_secret_key_for_flash_messages'

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction_history.csv')

def get_history():
    """Reads the prediction history from CSV file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    history.append(row)
        except Exception as e:
            print(f"[!] Error reading history file: {e}")
    # Return history in reverse order (newest first)
    return list(reversed(history))

def log_prediction(inputs, prediction_res):
    """Appends a new prediction entry to the CSV history file."""
    file_exists = os.path.exists(HISTORY_FILE)
    
    headers = [
        'Timestamp', 'Annual_Rainfall', 'Monsoon_Intensity', 'Cloud_Coverage',
        'Humidity', 'Temperature', 'River_Discharge', 'Probability', 'Result'
    ]
    
    try:
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Annual_Rainfall': inputs['Annual_Rainfall'],
                'Monsoon_Intensity': inputs['Monsoon_Intensity'],
                'Cloud_Coverage': inputs['Cloud_Coverage'],
                'Humidity': inputs['Humidity'],
                'Temperature': inputs['Temperature'],
                'River_Discharge': inputs['River_Discharge'],
                'Probability': f"{prediction_res['probability']}%",
                'Result': 'High Flood Risk' if prediction_res['prediction'] == 1 else 'Low Flood Risk'
            })
    except Exception as e:
        print(f"[!] Error writing to history file: {e}")

@app.route('/')
@app.route('/home')
def home():
    """Home / landing page."""
    model_trained = os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH)
    return render_template('index.html', model_trained=model_trained)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction form and result handler."""
    model_trained = os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH)
    
    if request.method == 'POST':
        if not model_trained:
            flash("Cannot make predictions because the model is not trained yet. Please train the model.", "danger")
            return redirect(url_for('predict'))
            
        # Retrieve form data
        form_data = request.form
        errors = {}
        
        # Validations (Backend double-check)
        fields = {
            'Annual_Rainfall': 'Annual Rainfall',
            'Monsoon_Intensity': 'Monsoon Intensity',
            'Cloud_Coverage': 'Cloud Coverage',
            'Humidity': 'Humidity',
            'Temperature': 'Temperature',
            'River_Discharge': 'River Discharge'
        }
        
        inputs = {}
        for key, name in fields.items():
            val = form_data.get(key, '').strip()
            if not val:
                errors[key] = f"{name} is required."
            else:
                try:
                    num_val = float(val)
                    if num_val < 0:
                        errors[key] = f"{name} cannot be negative."
                    inputs[key] = num_val
                except ValueError:
                    errors[key] = f"{name} must be a number."
                    
        if errors:
            return render_template('predict.html', errors=errors, form_data=form_data, model_trained=model_trained)
            
        # Execute prediction
        result = predict_flood(inputs)
        
        if result['success']:
            # Log to CSV
            log_prediction(form_data, result)
            
            # Map predictions to template variables
            prob = result['probability']
            pred = result['prediction']
            
            # Define preparedness recommendations
            recommendations = []
            if pred == 1:
                recommendations = [
                    "Evacuate from low-lying areas immediately if local authorities advise.",
                    "Pack an emergency go-bag (water, non-perishable food, flashlight, medication, documents).",
                    "Disconnect electrical appliances to avoid shocks and fire hazards.",
                    "Avoid walking or driving through flood waters (six inches of moving water can knock you down).",
                    "Establish a communication plan with family and stay tuned to local weather broadcasts."
                ]
            else:
                recommendations = [
                    "Weather parameters appear to be within normal safety limits.",
                    "Continue to monitor meteorological updates during monsoonal seasons.",
                    "Check clearance of storm drains and gutters around your home or neighborhood.",
                    "Maintain general weather preparedness kit and communication plans."
                ]
                
            return render_template(
                'result.html', 
                inputs=form_data, 
                probability=prob, 
                prediction=pred, 
                recommendations=recommendations,
                model_type=result['model_type']
            )
        else:
            flash(f"Prediction failed: {result['message']}", "danger")
            return redirect(url_for('predict'))
            
    return render_template('predict.html', model_trained=model_trained, form_data={})

@app.route('/about')
def about():
    """About page summarizing methodology, dataset schema, and training metrics."""
    # Check if images exist to see if model has been trained
    metrics_img_exists = os.path.exists(os.path.join(app.static_folder, 'images', 'model_comparison.png'))
    return render_template('about.html', metrics_img_exists=metrics_img_exists)

@app.route('/history')
def history():
    """History page that renders past predictions from prediction_history.csv."""
    records = get_history()
    return render_template('history.html', records=records)

@app.route('/download_history')
def download_history():
    """Download predictions log CSV."""
    if os.path.exists(HISTORY_FILE):
        return send_file(HISTORY_FILE, as_attachment=True, download_name='flood_prediction_history.csv')
    else:
        flash("No prediction history recorded yet.", "info")
        return redirect(url_for('history'))

@app.route('/clear_history')
def clear_history():
    """Clear all records from CSV."""
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
            flash("Prediction history cleared successfully.", "success")
        except Exception as e:
            flash(f"Failed to clear history: {e}", "danger")
    else:
        flash("History is already empty.", "info")
    return redirect(url_for('history'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with mock message submission."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        if not name or not email or not message:
            flash("All fields are required.", "danger")
        else:
            flash(f"Thank you, {name}! Your message has been sent successfully. We will get back to you shortly.", "success")
            return redirect(url_for('contact'))
            
    return render_template('contact.html')

# ================= Error Handling =================

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 handler."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 handler."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Bind to host '0.0.0.0' for deployment readiness
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
