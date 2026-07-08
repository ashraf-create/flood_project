# Phase 2: Requirement Analysis

This document outlines the software, hardware, functional, and non-functional requirements for the **Rising Waters** application.

---

## 1. System Requirements

### Hardware Requirements
- **Processor**: Dual-core Intel Core i3 or equivalent (minimum); Quad-core Intel Core i5/i7 or AMD Ryzen 5 (recommended for model training).
- **Memory**: 4 GB RAM (minimum); 8 GB RAM or more (recommended).
- **Storage**: 1 GB of available space for library installations, datasets, and generated plots.

### Software Requirements
- **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+).
- **Python Runtime**: Version 3.9, 3.10, or 3.11.
- **Package Installer**: pip.
- **Web Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari.

---

## 2. Functional Requirements
1. **Model Training**: The system must process CSV datasets, impute missing values, filter outliers using the Interquartile Range (IQR), and scale inputs.
2. **Classifier Comparison**: The pipeline must train Decision Tree, Random Forest, KNN, and XGBoost classifiers, evaluate metrics, and serialize the model with the highest F1-Score.
3. **Risk Inference**: The web server must expose a form to accept 6 weather observations, validate ranges, scale observations, and return predictions.
4. **Disaster Preparedness Action Plan**: The system must display custom safety warnings based on prediction risk.
5. **CSV Prediction Logging**: The application must save calculation transactions dynamically to a local CSV database.
6. **PDF Warning Report Exporter**: The client side must generate and download an A4 warning summary without hitting external network APIs.

---

## 3. Non-Functional Requirements
- **Performance**: Predict response times must be under 1.5 seconds.
- **Accuracy**: F1-Score of the selected classifier must exceed 85%.
- **Usability**: Responsive CSS design displaying a clean theme on desktop, laptop, and mobile screens.
- **Robustness**: Validation constraints on both client-side and server-side forms.
