# Rising Waters: A Machine Learning Approach to Flood Prediction

An intelligent, end-to-end flood prediction system leveraging historical meteorological and hydrological observations to assess flood risk.

---

## 📌 Abstract

Flooding is one of the most destructive natural disasters worldwide, causing extensive damage to infrastructure, loss of lives, and severe economic distress. Accurate and timely flood forecasting is critical for early warning systems and disaster management. 

This project implements an intelligent flood prediction system using classical and ensemble machine learning techniques. It trains and compares multiple classifiers—Decision Tree, Random Forest, K-Nearest Neighbors, and XGBoost—automatically serializing the model that achieves the highest F1-Score to handle class imbalances. The best-performing model is deployed via a responsive, premium Flask web interface, enabling users to input real-time weather indicators and receive instant risk probabilities, evacuation action plans, and downloadable PDF reports.

---

## 🎯 Problem Statement

Traditional flood prediction methods often rely purely on complex physical modeling of river basins, which requires intense computational resources and localized geological telemetry. These approaches often fail to provide:
1. **Real-time Accessibility**: Allowing field officers, local administrators, and citizens to get instant risk evaluations.
2. **Multi-Classifier Comparisons**: Selecting the single best model based on regional dataset characteristics rather than relying on a static, pre-chosen model.
3. **Actionable Outcomes**: Generating immediate evacuation checklists and warning reports along with predictions.

Our solution addresses these gaps by building a web-accessible, machine learning-driven risk assessment dashboard that processes raw meteorological indicators into actionable safety warnings.

---

## 🌟 Features

- **Multi-Model Pipeline**: Auto-evaluates Decision Tree, Random Forest, KNN, and XGBoost.
- **Automated Serialization**: Selects and saves the model with the highest F1-Score (currently **XGBoost** with an F1-Score of **0.8892**).
- **Outlier Filtering & Preprocessing**: Integrates IQR-based outlier detection, duplicate removal, median imputation, and standard scaling.
- **Visual Analytics Dashboard**: Exports correlation heatmaps, class distributions, model comparison metrics, and confusion heatmaps directly to the interface.
- **Persistent Prediction Logs**: Saves prediction transactions to a local CSV database, accessible via a responsive history table.
- **Zero-Dependency PDF Exporter**: Instant, client-side A4 PDF report generator showing weather inputs and emergency steps.
- **Robust Exception Handling**: Graceful warning pages when weights are missing and complete client/server form validations.

---

## 🛠️ Tech Stack

- **Backend Framework**: Python 3.10, Flask
- **Machine Learning**: Scikit-Learn, XGBoost, Joblib
- **Data Engineering**: Pandas, Numpy
- **Visualizations**: Matplotlib, Seaborn
- **Frontend UI**: Bootstrap 5, FontAwesome, Vanilla CSS
- **PDF Compilation**: jsPDF

---

## 📁 Folder Structure

Aligned to the reference internship submission template structure:

```
flood_project/
│
├── LICENSE                      # MIT License copyrights
├── README.md                    # Main Project README containing all requested sections
│
├── 1. Brainstorming & Ideation/
│   └── Brainstorming_and_Ideation.md # Project abstract, problem statement, objectives
│
├── 2. Requirement Analysis/
│   ├── Requirement_Analysis.md  # Software, hardware, functional/non-functional specs
│   └── requirements.txt         # Back-up copy of python libraries manifest
│
├── 3. Project Design Phase/
│   └── Project_Design.md        # System architecture flowchart and design details
│
├── 4. Project Planning Phase/
│   └── Project_Planning.md      # Milestones scheduling and developers work breakdown
│
├── 5. Project Development Phase/# Core Source Code Folder
│   ├── app.py                   # Flask server entry point
│   ├── train_model.py           # Preprocessing & ML training script
│   ├── prediction.py            # Inference model scaling wrapper
│   ├── requirements.txt         # Dependencies list
│   ├── runtime.txt              # Target Python runtime
│   ├── Procfile                 # Process deployment definition
│   ├── dataset/
│   │   └── flood.csv            # Historical dataset
│   ├── models/
│   │   ├── flood_model.pkl      # Best trained ML model weights
│   │   └── scaler.pkl           # Fitted standard scaler weights
│   ├── notebooks/
│   │   └── FloodPrediction.ipynb# Prototyping Jupyter notebook
│   ├── static/                  # Style sheets, JS scripting, and generated charts
│   └── templates/               # HTML view files
│
├── 6.Project Testing/
│   └── Project_Testing.md       # Front-end, server error-handling, and model metrics
│
├── 7.Project Documentation/
│   └── Project_Documentation.md  # Complete deployment and installation manuals
│
└── 8.Project Demonstration/
    ├── Project_Demonstration.md # Project demo URLs and presentation guide
    └── screenshots/             # Mockup visual layouts
        ├── landing_page.png
        ├── predict_form.png
        └── prediction_results.png
```

---

## 🚀 Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ashraf-create/flood_project.git
   cd flood_project
   ```

2. **Navigate to the Development Directory**:
   ```bash
   cd "5. Project Development Phase"
   ```

3. **Initialize a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💡 Usage Instructions

### 1. Train the Models
Ensure the training dataset [flood.csv](file:///c:/Users/satya/Downloads/flood_project/5.%20Project%20Development%20Phase/dataset/flood.csv) is present inside the development folder, and run:
```bash
python train_model.py
```
This trains the classifiers, serializes the best one to `models/`, and generates evaluation plots.

### 2. Start the App
Run the Flask server:
```bash
python app.py
```
Open a browser and navigate to **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**.

---

## 🤖 Machine Learning Models Used

During the training workflow, the pipeline automatically fits and compares four major classifiers on an 80/20 train/test split:
- **Decision Tree Classifier**: Fast baseline model.
- **Random Forest Classifier**: Robust ensemble bagging classifier.
- **K-Nearest Neighbors (KNN)**: Distance-based localized estimator.
- **XGBoost Classifier**: High-performance gradient boosting classifier.

The classifier achieving the highest **F1-Score** (currently **XGBoost** with an F1-Score of **0.8892**) is automatically selected and serialized for production inference.

---

## 📸 Screenshots Section

| View | Screenshot |
| :--- | :--- |
| **Landing Hero Page** | ![Data Page](<img width="1920" height="1080" alt="dashboard" src="https://github.com/user-attachments/assets/537a5203-c107-47c1-a0e2-d94f39de14ff" />
) |
| **Prediction Questionnaire** | ![Predict Form](<img width="1920" height="1080" alt="prediction" src="https://github.com/user-attachments/assets/29ac2333-3f64-4a25-9d4e-112a4d0a27ca" />
) |
| **Risk Analysis Result** | ![Prediction Results](<img width="1920" height="1080" alt="risk_analysis" src="https://github.com/user-attachments/assets/27d3b0ae-efb3-4a2f-9ab3-dea0f11c51d1" />
) |

---

## 🔮 Future Scope

- **Live Meteorological APIs**: Integrate third-party weather forecast APIs (e.g., OpenWeatherMap API) to fetch live local values automatically.
- **Geographical GIS mapping**: Integrate interactive maps (e.g., LeafletJS or Mapbox) showing flood zones and dynamic risk coordinates.
- **SMS Warning Alerts**: Integrate Twilio API to send evacuation warning texts to residents in high-probability risk areas.

---

## 👥 Team Members

- **Ashraf Mohammad** — Member
---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/satya/Downloads/flood_project/LICENSE) file for details.

##  🔗 Link
 🔗  https://flood-risk-predictor-s3nj.onrender.com
