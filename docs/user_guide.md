# User Guide

This guide details the setup and execution steps to run, train, and test the Rising Waters Flood Prediction System.

---

## 🛠️ Environment Prerequisites

- **Python**: Version 3.9, 3.10, or 3.11 is required.
- **Git** (Optional): For tracking changes and push/pull integrations.

---

## 🚀 Setting Up the Application

### 1. Initialize Virtual Environment
Open a terminal in the project directory and create an isolated environment:
```bash
python -m venv venv
```
Activate it:
- **Windows (PowerShell)**:
  ```bash
  .\venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. Install Python Dependencies
Install required packages using pip:
```bash
pip install -r requirements.txt
```

---

## 📊 Training the Machine Learning Engine

The system contains an automated training pipeline. To train the models and export weight binaries:
1. Ensure your source file `flood.csv` is placed under [dataset/](file:///c:/Users/satya/Downloads/flood_project/dataset). (I have already copied `flood_dataset.csv` there for you).
2. Execute the compilation script:
   ```bash
   python train_model.py
   ```
This will preprocess the dataset, train four classifiers, select the best one, export the weights to `models/`, and output metric plots to `static/images/`.

---

## 🖥️ Running the Flask App Locally

To start the Flask development server:
```bash
python app.py
```
Open a browser and navigate to:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 💡 Web App Workflow

### 1. Land on Home Page
- The Home page displays a system health banner indicating whether models have been trained.
- Click **Predict Risk** to start.

### 2. Fill the Weather Parameters Form
Input the values within valid ranges:
- **Annual Rainfall**: total regional annual precipitation (e.g. 1500 - 3500 mm).
- **Monsoon Intensity**: season wind force metric (e.g. 0 to 10).
- **Cloud Coverage**: percentage of cloud cover (0 to 100%).
- **Humidity**: atmospheric humidity levels (0 to 100%).
- **Temperature**: average ambient temp in °C (e.g. 15 to 45).
- **River Discharge**: river volume flow rate in $m^3/s$ (e.g. 100 to 800).

### 3. Review Results & Action Plan
- The Results page displays the prediction classification (High vs. Low Risk) along with the probability percentage.
- It displays a custom safety action plan depending on the risk severity.
- Click **Download PDF Report** to download an A4 format PDF warning summary.

### 4. Review Log History
- Navigate to **History Log** to see previous calculation entries, export them as a CSV, or clear the history logs.
