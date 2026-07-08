import os
import joblib
import numpy as np
import pandas as pd

# Set matplotlib to headless mode before importing pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

# Classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

# Path setups
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'flood.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def load_and_preprocess_data():
    """
    Loads dataset/flood.csv, handles missing values, removes duplicates,
    detects/filters outliers, scales features, and splits train/test.
    """
    print(f"[*] Loading dataset from: {DATASET_PATH}")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at '{DATASET_PATH}'. "
            f"Please place 'flood.csv' in the dataset/ folder and run again."
        )
        
    df = pd.read_csv(DATASET_PATH)
    print(f"[+] Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # 1. Handle Missing Values
    null_counts = df.isnull().sum().sum()
    if null_counts > 0:
        print(f"[!] Found {null_counts} missing values. Imputing with column median...")
        for col in df.columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())
    else:
        print("[+] No missing values detected.")
        
    # 2. Remove Duplicates
    dup_counts = df.duplicated().sum()
    if dup_counts > 0:
        print(f"[!] Found {dup_counts} duplicate records. Removing them...")
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"[+] Dataset shape after duplicate removal: {df.shape[0]} rows.")
    else:
        print("[+] No duplicate records detected.")
        
    # Columns matching user's schema
    features = ['Annual_Rainfall', 'Monsoon_Intensity', 'Cloud_Coverage', 
                'Humidity', 'Temperature', 'River_Discharge']
    target = 'Flood'
    
    # Verify columns exist
    missing_cols = [c for c in features + [target] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in dataset: {missing_cols}")

    # Save distribution plot of target before filtering outliers
    plot_flood_distribution(df, target)
    
    # 3. Outlier Detection and Filtering using IQR
    print("[*] Performing outlier detection using IQR on numerical features...")
    original_row_count = df.shape[0]
    
    # Keep track of indices that are outliers
    outlier_mask = pd.Series(False, index=df.index)
    for col in features:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Mark outliers
        col_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_mask = outlier_mask | col_outliers
        
    outliers_count = outlier_mask.sum()
    if outliers_count > 0:
        print(f"[!] Detected {outliers_count} outliers. Removing from training set...")
        df = df[~outlier_mask].reset_index(drop=True)
        removed_percentage = (outliers_count / original_row_count) * 100
        print(f"[+] Outlier filtering complete. Removed {removed_percentage:.2f}% of rows. "
              f"Remaining rows: {df.shape[0]}.")
    else:
        print("[+] No outliers detected.")

    # Save correlation heatmap
    plot_correlation_heatmap(df, features + [target])
    
    # Extract features (X) and target (y)
    X = df[features]
    y = df[target]
    
    # 4. Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[+] Split dataset: Train shape={X_train.shape}, Test shape={X_test.shape}")
    
    # 5. Feature Scaling using StandardScaler
    print("[*] Fitting StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler immediately
    scaler_save_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    joblib.dump(scaler, scaler_save_path)
    print(f"[+] Saved scaler to {scaler_save_path}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, features, scaler

# ================= EDA Plotting Functions =================

def plot_flood_distribution(df, target_col):
    """Generates and saves the Flood distribution count plot."""
    plt.figure(figsize=(6, 5))
    # Countplot
    sns.countplot(x=target_col, data=df, palette=['#1a80b8', '#d9534f'])
    plt.title('Flood Target Distribution (0: No Flood, 1: Flood)', fontsize=14, pad=15)
    plt.xlabel('Flood Class', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks([0, 1], ['No Flood (0)', 'Flood (1)'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plot_path = os.path.join(IMAGES_DIR, 'flood_distribution.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

def plot_correlation_heatmap(df, cols):
    """Generates and saves the Correlation Heatmap."""
    plt.figure(figsize=(8, 7))
    correlation_matrix = df[cols].corr()
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='Blues', 
        fmt=".2f", 
        linewidths=0.5,
        cbar_kws={'shrink': 0.8}
    )
    plt.title('Feature Correlation Matrix', fontsize=14, pad=15)
    plt.tight_layout()
    plot_path = os.path.join(IMAGES_DIR, 'correlation_heatmap.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

def plot_feature_importance(model, feature_names):
    """Generates and saves feature importance graph for tree-based models."""
    plt.figure(figsize=(8, 6))
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        sorted_features = [feature_names[i] for i in indices]
        sorted_importances = importances[indices]
        
        sns.barplot(x=sorted_importances, y=sorted_features, palette='Blues_r')
        plt.title('Feature Importances for Flood Prediction', fontsize=14, pad=15)
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
    else:
        # Fallback if model doesn't support feature_importances_ (e.g. KNN)
        plt.text(0.5, 0.5, 'Feature Importance not available for the best model', 
                 ha='center', va='center', fontsize=12)
    
    plot_path = os.path.join(IMAGES_DIR, 'feature_importance.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

def plot_model_comparison(results_df):
    """Generates and saves model comparison bar chart."""
    plt.figure(figsize=(10, 6))
    # Melt dataframe for easier plotting with seaborn
    melted_df = pd.melt(results_df, id_vars=['Model'], value_vars=['Accuracy', 'Precision', 'Recall', 'F1-Score'])
    
    sns.barplot(x='Model', y='value', hue='variable', data=melted_df, palette='Blues')
    plt.title('Model Performance Comparison', fontsize=14, pad=15)
    plt.xlabel('Machine Learning Model', fontsize=12)
    plt.ylabel('Score (0.0 - 1.0)', fontsize=12)
    plt.ylim(0, 1.1)
    plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plot_path = os.path.join(IMAGES_DIR, 'model_comparison.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

def plot_confusion_matrix_heatmap(y_true, y_pred, model_name):
    """Generates and saves the confusion matrix plot for the best model."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt="d", 
        cmap='Blues', 
        cbar=False,
        xticklabels=['No Flood (0)', 'Flood (1)'],
        yticklabels=['No Flood (0)', 'Flood (1)']
    )
    plt.title(f'Confusion Matrix: {model_name} (Best Model)', fontsize=14, pad=15)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.tight_layout()
    
    plot_path = os.path.join(IMAGES_DIR, 'confusion_matrix.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

def plot_roc_curves(trained_models, X_test, y_test):
    """Generates and saves ROC curves comparison plot."""
    plt.figure(figsize=(8, 6))
    for name, model in trained_models.items():
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, probs)
            auc = roc_auc_score(y_test, probs)
            plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})")
            
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing (AUC = 0.500)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curves', fontsize=14, pad=15)
    plt.legend(loc="lower right")
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plot_path = os.path.join(IMAGES_DIR, 'roc_curve.png')
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"[+] Saved plot: {plot_path}")

# ================= Training & Evaluation Layer =================

def train_and_evaluate():
    """
    Main training pipeline. Fits all four classifiers, compares performance metrics,
    selects the best model based on F1-Score, generates plots and serializes files.
    """
    try:
        # Load and preprocess
        X_train, X_test, y_train, y_test, feature_names, scaler = load_and_preprocess_data()
    except FileNotFoundError as e:
        print(f"\n[!] ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n[!] Unexpected preprocessing error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    print("\n[*] Initializing machine learning classifiers...")
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=8, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced'),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss', scale_pos_weight=1.5)
    }
    
    # Store performance metrics
    results = []
    trained_models = {}
    
    for name, clf in models.items():
        print(f"[*] Training {name} Classifier...")
        clf.fit(X_train, y_train)
        trained_models[name] = clf
        
        # Predict on test set
        y_pred = clf.predict(X_test)
        
        # Get probabilities for ROC-AUC
        if hasattr(clf, "predict_proba"):
            y_probs = clf.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_probs)
        else:
            auc = 0.5  # default if not available
            
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        print(f"    - Accuracy : {acc:.4f}")
        print(f"    - Precision: {prec:.4f}")
        print(f"    - Recall   : {rec:.4f}")
        print(f"    - F1-Score : {f1:.4f}")
        print(f"    - ROC-AUC  : {auc:.4f}")
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'ROC-AUC': auc
        })
        
    results_df = pd.DataFrame(results)
    
    # Print comparison table in CLI
    print("\n" + "="*80)
    print("                      MODEL PERFORMANCE COMPARISON")
    print("="*80)
    print(results_df.to_string(index=False))
    print("="*80)
    
    # Plot Model Performance Comparison
    plot_model_comparison(results_df)
    
    # Plot ROC Curves
    plot_roc_curves(trained_models, X_test, y_test)
    
    # Find Best Model (maximizing F1-Score since flood datasets are often imbalanced)
    best_idx = results_df['F1-Score'].idxmax()
    best_model_name = results_df.loc[best_idx, 'Model']
    best_f1 = results_df.loc[best_idx, 'F1-Score']
    best_clf = trained_models[best_model_name]
    
    print(f"\n[+] Automatic Selection: '{best_model_name}' is the best model with F1-Score: {best_f1:.4f}")
    
    # Save the Best Model
    model_save_path = os.path.join(MODELS_DIR, 'flood_model.pkl')
    joblib.dump(best_clf, model_save_path)
    print(f"[+] Saved best model to: {model_save_path}")
    
    # Generate Best Model specific plots
    # 1. Confusion Matrix
    y_pred_best = best_clf.predict(X_test)
    plot_confusion_matrix_heatmap(y_test, y_pred_best, best_model_name)
    
    # 2. Feature Importance
    plot_feature_importance(best_clf, feature_names)
    
    print("\n[+] ML Pipeline Completed Successfully! All metrics logged and visualizations generated.")
    return True

if __name__ == '__main__':
    train_and_evaluate()
