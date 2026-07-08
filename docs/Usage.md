# Usage Instructions

Follow these instructions to run the model training pipeline and launch the web server:

### 1. Place the Dataset
Ensure your target dataset `flood.csv` is saved under the [dataset/](file:///c:/Users/satya/Downloads/flood_project/dataset) directory:
- Expected schema includes meteorological features (`Annual_Rainfall`, `Monsoon_Intensity`, `Cloud_Coverage`, `Humidity`, `Temperature`, `River_Discharge`) and a target feature (`Flood` binary classifier).

### 2. Train the Machine Learning Pipeline
Before starting the web server, run the model compiler script to fit the scaler and serialize the best classifier:
```bash
python train_model.py
```
This runs preprocessing, fits the standardizer, trains the four models (Decision Tree, Random Forest, KNN, XGBoost), selects the highest F1-Score model, and exports static evaluation plots.

### 3. Start the Flask Server
Run the Flask server:
```bash
python app.py
```
Open a browser and navigate to:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

### 4. Interactive Flow
1. Navigate to **Predict Risk** and input weather observations.
2. Click **Run Risk Prediction** to view the output probability and action plan.
3. Click **Download PDF Report** to download an offline warning report.
4. Navigate to **History Log** to view past prediction queries, download them as a CSV, or clear logs.
