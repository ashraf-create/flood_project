# Abstract

Flooding is a catastrophic meteorological and hydrological event that poses an immense threat to human lives, infrastructure, and regional economies. Climate change has exacerbated the frequency and intensity of monsoons, rendering traditional heuristic forecasting models inadequate. 

This project presents **Rising Waters**, a machine learning-based flood prediction system. By analyzing historical environmental indicators—including annual rainfall, monsoon intensity, cloud coverage, humidity, temperature, and river discharge—the system acts as an early warning hazard assessment tool. 

The pipeline trains and evaluates four distinct machine learning classifiers:
1. **Decision Tree Classifier**
2. **Random Forest Classifier**
3. **K-Nearest Neighbors (KNN)**
4. **XGBoost Classifier**

The training pipeline automatically compares these models and serializes the classifier achieving the highest F1-Score to ensure high classification reliability. This model is served via a premium, responsive web interface built using Flask, enabling local administrative authorities and emergency response agencies to evaluate hydrological parameters, check persistent warning logs, and download warning reports.
