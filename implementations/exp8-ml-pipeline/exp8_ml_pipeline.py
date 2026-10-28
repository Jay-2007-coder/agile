"""
Experiment 8: ML Pipeline with MLflow - House Price Prediction
================================================================
AIM: Build a complete ML pipeline using sklearn Pipeline + MLflow
     for tracking, model comparison, and deployment.

Dataset: California Housing Dataset (Regression)
Models: Linear Regression, Ridge Regression, Random Forest Regressor
Metrics: RMSE, MAE, R² Score

Setup:
  pip install mlflow scikit-learn pandas numpy matplotlib seaborn

Run:
  python exp8_ml_pipeline.py
  mlflow ui  (then open http://localhost:5000)
"""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# MLflow Experiment Setup
# ============================================================
EXPERIMENT_NAME = "House_Price_ML_Pipeline_Exp8"
mlflow.set_experiment(EXPERIMENT_NAME)

print("="*60)
print("  Experiment 8: ML Pipeline with MLflow")
print("="*60)

# ============================================================
# STEP 1: Load Dataset
# ============================================================
print("\n[STEP 1] Loading California Housing Dataset...")
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = housing.target

print(f"  Features: {list(X.columns)}")
print(f"  Samples: {len(X)}")
print(f"  Target range: ${y.min():.2f} - ${y.max():.2f} (x $100,000)")
print(f"\n  Data Statistics:\n{X.describe().round(2)}")

# ============================================================
# STEP 2: Preprocessing
# ============================================================
print("\n[STEP 2] Splitting and preprocessing data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

# ============================================================
# STEP 3: Define Pipelines
# ============================================================
pipelines = {
    "Linear_Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "Ridge_Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ]),
    "Lasso_Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Lasso(alpha=0.1))
    ]),
    "Random_Forest": Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ]),
    "Gradient_Boosting": Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
    ])
}

pipeline_params = {
    "Linear_Regression": {"model": "LinearRegression", "alpha": "N/A"},
    "Ridge_Regression": {"model": "Ridge", "alpha": 1.0},
    "Lasso_Regression": {"model": "Lasso", "alpha": 0.1},
    "Random_Forest": {"model": "RandomForest", "n_estimators": 100, "max_depth": "auto"},
    "Gradient_Boosting": {"model": "GradientBoosting", "n_estimators": 100, "learning_rate": 0.1}
}

# ============================================================
# STEP 4: Train Pipelines and Log to MLflow
# ============================================================
print("\n[STEP 4] Training pipelines and logging to MLflow...")
results = []

for name, pipeline in pipelines.items():
    print(f"\n  Training {name}...")

    with mlflow.start_run(run_name=name):
        # Tags
        mlflow.set_tag("model_name", name)
        mlflow.set_tag("task", "regression")
        mlflow.set_tag("dataset", "California_Housing")
        mlflow.set_tag("author", "Jay Student")

        # Params
        params = pipeline_params[name]
        params["test_size"] = 0.2
        params["pipeline_steps"] = "StandardScaler -> Model"
        mlflow.log_params(params)

        # Train
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        cv_scores = cross_val_score(
            pipeline, X_train, y_train, cv=5,
            scoring='neg_root_mean_squared_error', n_jobs=-1
        )
        cv_rmse = -cv_scores.mean()

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("cv_rmse", cv_rmse)

        # Log model
        mlflow.sklearn.log_model(
            pipeline,
            artifact_path=f"pipeline/{name}",
            registered_model_name=f"HousePricePipeline_{name}"
        )

        # Prediction vs Actual plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Scatter plot
        axes[0].scatter(y_test[:200], y_pred[:200], alpha=0.5, s=20)
        axes[0].plot([y_test.min(), y_test.max()],
                     [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[0].set_xlabel("Actual Price")
        axes[0].set_ylabel("Predicted Price")
        axes[0].set_title(f"{name} - Actual vs Predicted")

        # Residual plot
        residuals = y_test - y_pred
        axes[1].hist(residuals, bins=50, edgecolor='black', alpha=0.7)
        axes[1].axvline(0, color='red', linestyle='--')
        axes[1].set_xlabel("Residuals")
        axes[1].set_ylabel("Frequency")
        axes[1].set_title(f"{name} - Residual Distribution")

        plt.suptitle(f"{name} | RMSE={rmse:.4f} | R²={r2:.4f}", fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{name}_analysis.png", dpi=100)
        mlflow.log_artifact(f"{name}_analysis.png")
        plt.close()

        print(f"    RMSE: {rmse:.4f}")
        print(f"    MAE:  {mae:.4f}")
        print(f"    R²:   {r2:.4f}")
        print(f"    CV RMSE: {cv_rmse:.4f}")

        results.append({
            "Model": name,
            "RMSE": rmse,
            "MAE": mae,
            "R2_Score": r2,
            "CV_RMSE": cv_rmse
        })

# ============================================================
# STEP 5: Summary
# ============================================================
print("\n[STEP 5] Results Summary:")
results_df = pd.DataFrame(results).sort_values("R2_Score", ascending=False)
print(results_df.to_string(index=False))

with mlflow.start_run(run_name="Pipeline_Comparison_Summary"):
    mlflow.set_tag("type", "summary")
    best = results_df.iloc[0]
    mlflow.log_param("best_pipeline", best["Model"])
    mlflow.log_metric("best_r2", best["R2_Score"])
    mlflow.log_metric("best_rmse", best["RMSE"])
    results_df.to_csv("pipeline_comparison.csv", index=False)
    mlflow.log_artifact("pipeline_comparison.csv")

    # Bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(results_df["Model"], results_df["R2_Score"],
           color=['green' if x > 0.7 else 'orange' for x in results_df["R2_Score"]])
    ax.set_ylabel("R² Score (higher is better)")
    ax.set_title("Pipeline R² Score Comparison")
    plt.xticks(rotation=15)
    for i, (_, row) in enumerate(results_df.iterrows()):
        ax.text(i, row["R2_Score"] + 0.005, f"{row['R2_Score']:.3f}", ha='center')
    plt.tight_layout()
    plt.savefig("pipeline_r2_comparison.png", dpi=100)
    mlflow.log_artifact("pipeline_r2_comparison.png")
    plt.close()

print("\n" + "="*60)
print(f"  Best Pipeline: {results_df.iloc[0]['Model']}")
print(f"  Best R²: {results_df.iloc[0]['R2_Score']:.4f}")
print(f"  Best RMSE: {results_df.iloc[0]['RMSE']:.4f}")
print("="*60)
print("\nView in MLflow UI: mlflow ui → http://localhost:5000")
print("Experiment 8 Complete!")
