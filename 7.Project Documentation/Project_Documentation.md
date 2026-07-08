# Phase 7: Project Documentation

This document serves as the operational guide and deployment manual for the **Rising Waters** application.

---

## 🚀 Installation & Set Up

### 1. Prerequisites
- **Python**: Version 3.9, 3.10, or 3.11.
- Ensure terminal access is active in the [5. Project Development Phase/](file:///c:/Users/satya/Downloads/flood_project/5.%20Project%20Development%20Phase) folder.

### 2. Set Up a Virtual Environment
Create and activate an isolated environment inside the development folder:
```bash
cd "5. Project Development Phase"
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install Python libraries:
```bash
pip install -r requirements.txt
```

---

## 📊 Training Pipeline Compilation

Before starting the web server, you must compile model weights and evaluation plots:
1. Ensure `dataset/flood.csv` is present in the development folder.
2. Run the compiler:
   ```bash
   python train_model.py
   ```
This Preprocesses the dataset, evaluates model statistics, saves `flood_model.pkl` and `scaler.pkl` to `models/`, and generates charts under `static/images/`.

---

## 🖥️ Running the Flask Application

Start the Flask server locally:
```bash
python app.py
```
Open a browser and navigate to:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## ☁️ Production Deployment

The project is deployment-ready for cloud platforms like **IBM Cloud Code Engine**:
1. Log in to the IBM Cloud CLI and target your resource group:
   ```bash
   ibmcloud login -a cloud.ibm.com
   ibmcloud target -g Default
   ```
2. Deploy directly from the source development directory:
   ```bash
   ibmcloud ce app create --name rising-waters-app --build-source . --port 5000
   ```
Code Engine will compile the app using the `Procfile` and bind it to a public domain automatically.
