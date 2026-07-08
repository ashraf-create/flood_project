# Phase 6: Project Testing

This document details the test plans, validation criteria, and model evaluation metrics for the **Rising Waters** application.

---

## 1. Front-End Validation Tests
To prevent system failures, interactive forms are bounded using JavaScript input validations:
- **Numerical Validation**: Rejects alphabetical inputs.
- **Boundary Limits**: Validates percentage inputs to a maximum range of 100% (specifically for `Cloud_Coverage` and `Humidity`).
- **Sign Bounds**: Barrows submissions containing negative inputs (raises validation errors).
- **Empty Fields check**: Submits form inputs only if all fields contain numbers.

---

## 2. Server-Side Exception Handling Tests
- **Missing Weight Files**: If `models/flood_model.pkl` or `models/scaler.pkl` are deleted, the application loads a warning block in the calculation questionnaire, disabling the submit button.
- **Incorrect Parameters**: If the user submits requests containing negative values via custom curl scripts, the server returns inline Flask messages rather than throwing exceptions.
- **Error Pages**: Integrated custom templates for `404 Not Found` and `500 Server Error` exceptions.

---

## 3. Model Comparison & Training Evaluation Metrics

The classification algorithms were evaluated on a test split of 600 observations (from a total dataset of 3,000 observations):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **XGBoost Classifier** | **0.8733** | **0.8997** | **0.8790** | **0.8892** | **0.9485** |
| **Random Forest Classifier** | 0.8717 | 0.8994 | 0.8761 | 0.8876 | 0.9503 |
| **K-Nearest Neighbors (KNN)** | 0.8500 | 0.8746 | 0.8646 | 0.8696 | 0.9313 |
| **Decision Tree Classifier** | 0.8367 | 0.8952 | 0.8127 | 0.8520 | 0.8871 |

### Outlier Filtering (IQR Check)
No extreme outliers were detected during training because values were filtered within:
$$[Q1 - 1.5 \times \text{IQR},\ Q3 + 1.5 \times \text{IQR}]$$
This ensures distance-based algorithms like K-Nearest Neighbors perform classification reliably.
