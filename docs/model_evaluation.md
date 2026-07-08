# Model Evaluation and Analysis Report

This document reports the performance metrics and training evaluation results of the classifier models compiled by the training pipeline.

---

## Dataset Overview

- **Source File**: `dataset/flood.csv`
- **Total Samples**: 3,000 observations
- **Target Feature**: `Flood` (Binary Classification: `0 = Low Risk`, `1 = High Risk`)
- **Features Used**:
  - `Annual_Rainfall`
  - `Monsoon_Intensity`
  - `Cloud_Coverage`
  - `Humidity`
  - `Temperature`
  - `River_Discharge`

---

## Training Evaluation Metrics

The pipeline split the dataset into **80% Training** (2,400 samples) and **20% Testing** (600 samples) sets. Below are the performance results calculated on the independent test split:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **XGBoost** | **0.8733** | **0.8997** | **0.8790** | **0.8892** | **0.9485** |
| **Random Forest** | 0.8717 | 0.8994 | 0.8761 | 0.8876 | 0.9503 |
| **K-Nearest Neighbors** | 0.8500 | 0.8746 | 0.8646 | 0.8696 | 0.9313 |
| **Decision Tree** | 0.8367 | 0.8952 | 0.8127 | 0.8520 | 0.8871 |

### Performance Visualization Charts
During compiling, the script automatically exports the following charts to `static/images/`:
1. `flood_distribution.png`: Evaluates balancing of the target variable.
2. `correlation_heatmap.png`: Highlighting multicollinearity index.
3. `model_comparison.png`: Comparison graphs across accuracy, recall, and F1 metrics.
4. `roc_curve.png`: Graphing True Positive vs. False Positive ratios.
5. `confusion_matrix.png`: Breakdown of True/False predictions.
6. `feature_importance.png`: Importance scores of variables.

---

## Model Selection Details

- **Selected Model**: **XGBoost Classifier**
- **Reasoning**: The selection mechanism evaluates the highest **F1-Score** on the validation set, ensuring balance between Precision and Recall. XGBoost achieved the highest F1-Score of **0.8892** and was serialized as `models/flood_model.pkl`.
