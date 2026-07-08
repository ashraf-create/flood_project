# Features

The **Rising Waters** application is configured with several high-performance features across its training, inference, and presentation layers:

- **End-to-End ML Training Pipeline**: Reads raw datasets, handles null inputs using column medians, filters outliers via the Interquartile Range (IQR) method, scales variables, and trains multiple classifiers.
- **Automated Model Selection**: Evaluates model performance across Accuracy, Precision, Recall, F1-Score, and ROC-AUC metrics. Serializes the model with the highest F1-Score (currently **XGBoost** with an F1-Score of **0.8892**).
- **Interactive Web Interface**: A premium ocean-blue dashboard incorporating responsive Bootstrap grids and clean visual badges.
- **Client-Side PDF Report Generator**: Compiles weather parameters, warning classifications, and custom action plans into an A4 PDF report for instant download.
- **Persistent Transaction Logs**: Saves every prediction query to a local CSV log, allowing users to view, export, or clear history entries dynamically.
- **Robust Client & Server Validations**: Restricts forms from negative values, ensures numeric limits, and locks input forms if model weights are missing.
