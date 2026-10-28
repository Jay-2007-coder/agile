"""
Experiment 7: MLflow - Machine Learning Experiment Tracking
=============================================================
AIM: To understand and implement experiment tracking using MLflow
     for a machine learning model.

Dataset: Iris Dataset (Classification)
Models: Logistic Regression, Random Forest, Decision Tree
Metrics: Accuracy, Precision, Recall, F1-Score

Setup:
  pip install mlflow scikit-learn pandas numpy matplotlib seaborn

Run:
  python exp7_mlflow_tracking.py
  mlflow ui  (then open http://localhost:5000)
"""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# SETUP MLFLOW
# ============================================================
EXPERIMENT_NAME = "Iris_Classification_Experiment7"
mlflow.set_experiment(EXPERIMENT_NAME)

print("="*60)
print("  Experiment 7: MLflow Experiment Tracking")
print("="*60)

# ============================================================
# STEP 1: Load and Explore Dataset
# ============================================================
print("\n[STEP 1] Loading Iris Dataset...")
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

df = pd.DataFrame(X, columns=feature_names)
df['species'] = [target_names[i] for i in y]

print(f"  Dataset shape: {X.shape}")
print(f"  Features: {feature_names}")
print(f"  Classes: {target_names}")
print(f"  Class distribution:\n{df['species'].value_counts()}")
print(f"\n  First 5 rows:\n{df.head()}")

# ============================================================
# STEP 2: Preprocessing
# ============================================================
print("\n[STEP 2] Preprocessing...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"  Training samples: {len(X_train)}")
print(f"  Test samples: {len(X_test)}")

# ============================================================
# STEP 3: Define Models to Compare
# ============================================================
models = {
    "Logistic_Regression": {
        "model": LogisticRegression(max_iter=1000, random_state=42),
        "params": {"max_iter": 1000, "solver": "lbfgs", "C": 1.0}
    },
    "Random_Forest": {
        "model": RandomForestClassifier(n_estimators=100, random_state=42),
        "params": {"n_estimators": 100, "max_depth": None, "random_state": 42}
    },
    "Decision_Tree": {
        "model": DecisionTreeClassifier(max_depth=5, random_state=42),
        "params": {"max_depth": 5, "criterion": "gini", "random_state": 42}
    },
    "SVM": {
        "model": SVC(kernel='rbf', C=1.0, random_state=42),
        "params": {"kernel": "rbf", "C": 1.0, "gamma": "scale"}
    }
}

# ============================================================
# STEP 4: Train Models and Log with MLflow
# ============================================================
print("\n[STEP 4] Training models and logging to MLflow...")
results = []

for model_name, config in models.items():
    print(f"\n  Training {model_name}...")

    with mlflow.start_run(run_name=model_name):
        # --- Log tags ---
        mlflow.set_tag("model_type", model_name)
        mlflow.set_tag("dataset", "Iris")
        mlflow.set_tag("experiment_phase", "comparison")
        mlflow.set_tag("author", "Jay Student")

        # --- Log parameters ---
        mlflow.log_params(config["params"])
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("scaling", "StandardScaler")

        # --- Train model ---
        model = config["model"]
        model.fit(X_train_scaled, y_train)

        # --- Predict ---
        y_pred = model.predict(X_test_scaled)

        # --- Calculate metrics ---
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()

        # --- Log metrics ---
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("cv_mean", cv_mean)
        mlflow.log_metric("cv_std", cv_std)

        # --- Log model ---
        mlflow.sklearn.log_model(
            model,
            artifact_path=f"models/{model_name}",
            registered_model_name=f"IrisClassifier_{model_name}"
        )

        # --- Create and log confusion matrix plot ---
        fig, ax = plt.subplots(figsize=(8, 6))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(
            cm, annot=True, fmt='d', ax=ax,
            xticklabels=target_names,
            yticklabels=target_names,
            cmap='Blues'
        )
        ax.set_title(f"Confusion Matrix - {model_name}")
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(f"{model_name}_confusion_matrix.png", dpi=100)
        mlflow.log_artifact(f"{model_name}_confusion_matrix.png")
        plt.close()

        # --- Log classification report as text ---
        report = classification_report(y_test, y_pred, target_names=target_names)
        with open(f"{model_name}_report.txt", "w") as f:
            f.write(f"Model: {model_name}\n")
            f.write("="*50 + "\n")
            f.write(report)
        mlflow.log_artifact(f"{model_name}_report.txt")

        print(f"    Accuracy:  {accuracy:.4f}")
        print(f"    Precision: {precision:.4f}")
        print(f"    Recall:    {recall:.4f}")
        print(f"    F1-Score:  {f1:.4f}")
        print(f"    CV Mean:   {cv_mean:.4f} (±{cv_std:.4f})")

        results.append({
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1_Score": f1,
            "CV_Mean": cv_mean,
            "CV_Std": cv_std
        })

# ============================================================
# STEP 5: Compare Results
# ============================================================
print("\n[STEP 5] Model Comparison:")
results_df = pd.DataFrame(results).sort_values("Accuracy", ascending=False)
print(results_df.to_string(index=False))

# Log comparison results
with mlflow.start_run(run_name="Model_Comparison_Summary"):
    mlflow.set_tag("type", "comparison_summary")

    # Best model
    best_model = results_df.iloc[0]
    mlflow.log_param("best_model", best_model["Model"])
    mlflow.log_metric("best_accuracy", best_model["Accuracy"])

    # Save comparison table
    results_df.to_csv("model_comparison.csv", index=False)
    mlflow.log_artifact("model_comparison.csv")

    # Comparison bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ["Accuracy", "Precision", "Recall", "F1_Score"]
    x = np.arange(len(results_df))
    width = 0.2

    for i, metric in enumerate(metrics):
        ax.bar(x + i * width, results_df[metric], width, label=metric)

    ax.set_xlabel("Models")
    ax.set_ylabel("Score")
    ax.set_title("Model Performance Comparison")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(results_df["Model"], rotation=15)
    ax.legend()
    ax.set_ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig("model_comparison.png", dpi=100)
    mlflow.log_artifact("model_comparison.png")
    plt.close()

print("\n" + "="*60)
print(f"  Best Model: {results_df.iloc[0]['Model']}")
print(f"  Best Accuracy: {results_df.iloc[0]['Accuracy']:.4f}")
print("="*60)
print("\nMLflow UI: Run 'mlflow ui' and open http://localhost:5000")
print("Experiment 7 Complete!")
