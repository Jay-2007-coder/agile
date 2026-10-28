"""
Experiment 9: Student Performance Prediction with MLflow
==========================================================
AIM: Build and track ML models to predict student exam scores
     using MLflow for experiment tracking and model registry.

Dataset: Student Performance Dataset (CSV generated here)
Features: Study_Hours, Attendance%, Previous_Score, Sleep_Hours, Practice_Tests
Target: Final_Exam_Score (0-100)

Models: Linear Regression, Decision Tree, Random Forest, Gradient Boosting
Metrics: MAE, RMSE, R² Score

Setup:
  pip install mlflow scikit-learn pandas numpy matplotlib seaborn

Run:
  python exp9_student_performance.py
  mlflow ui  → http://localhost:5000
"""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: Generate/Load Dataset
# ============================================================
np.random.seed(42)
N = 1000  # Number of students

print("="*60)
print("  Experiment 9: Student Performance Prediction")
print("="*60)

print("\n[STEP 1] Generating Student Performance Dataset...")

study_hours = np.random.uniform(1, 10, N)
attendance = np.random.uniform(50, 100, N)
previous_score = np.random.uniform(40, 95, N)
sleep_hours = np.random.uniform(4, 9, N)
practice_tests = np.random.randint(0, 15, N)
gender = np.random.choice(['Male', 'Female'], N)
internet_access = np.random.choice(['Yes', 'No'], N)
tutoring_sessions = np.random.randint(0, 10, N)

# Target: Final exam score (weighted combination + noise)
final_score = (
    study_hours * 3.5 +
    attendance * 0.3 +
    previous_score * 0.4 +
    sleep_hours * 1.5 +
    practice_tests * 1.2 +
    tutoring_sessions * 1.8 +
    np.random.normal(0, 3, N)
)
# Normalize to 0-100 range
final_score = np.clip(
    (final_score - final_score.min()) / (final_score.max() - final_score.min()) * 100,
    0, 100
)

df = pd.DataFrame({
    'Study_Hours': study_hours,
    'Attendance_Percent': attendance,
    'Previous_Score': previous_score,
    'Sleep_Hours': sleep_hours,
    'Practice_Tests': practice_tests,
    'Tutoring_Sessions': tutoring_sessions,
    'Gender': gender,
    'Internet_Access': internet_access,
    'Final_Score': final_score.round(2)
})

# Save dataset
df.to_csv("student_performance.csv", index=False)
print(f"  Generated {N} student records")
print(f"  Features: {list(df.columns[:-1])}")
print(f"  Target: Final_Score (range: {df['Final_Score'].min():.1f} - {df['Final_Score'].max():.1f})")
print(f"\n  Dataset preview:\n{df.head()}")
print(f"\n  Statistics:\n{df.describe().round(2)}")

# ============================================================
# STEP 2: Exploratory Data Analysis (EDA)
# ============================================================
print("\n[STEP 2] Exploratory Data Analysis...")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

# Score distribution
axes[0].hist(df['Final_Score'], bins=30, edgecolor='black', color='skyblue', alpha=0.7)
axes[0].set_title('Final Score Distribution')
axes[0].set_xlabel('Score')
axes[0].set_ylabel('Frequency')

# Study hours vs Score
axes[1].scatter(df['Study_Hours'], df['Final_Score'], alpha=0.4, s=10)
axes[1].set_title('Study Hours vs Final Score')
axes[1].set_xlabel('Study Hours per Day')
axes[1].set_ylabel('Final Score')

# Attendance vs Score
axes[2].scatter(df['Attendance_Percent'], df['Final_Score'], alpha=0.4, s=10, color='orange')
axes[2].set_title('Attendance vs Final Score')
axes[2].set_xlabel('Attendance (%)')

# Previous score vs Final score
axes[3].scatter(df['Previous_Score'], df['Final_Score'], alpha=0.4, s=10, color='green')
axes[3].set_title('Previous Score vs Final Score')
axes[3].set_xlabel('Previous Score')

# Gender distribution
gender_scores = df.groupby('Gender')['Final_Score'].mean()
axes[4].bar(gender_scores.index, gender_scores.values, color=['steelblue', 'salmon'])
axes[4].set_title('Average Score by Gender')
axes[4].set_ylabel('Average Final Score')

# Correlation heatmap
numeric_cols = ['Study_Hours', 'Attendance_Percent', 'Previous_Score',
                'Sleep_Hours', 'Practice_Tests', 'Tutoring_Sessions', 'Final_Score']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[5], center=0)
axes[5].set_title('Feature Correlation Heatmap')

plt.suptitle('Student Performance - Exploratory Data Analysis', fontsize=14)
plt.tight_layout()
plt.savefig("eda_plots.png", dpi=100)
plt.close()
print("  EDA plots saved: eda_plots.png")

# ============================================================
# STEP 3: Preprocessing
# ============================================================
print("\n[STEP 3] Preprocessing...")

# Encode categorical features
le = LabelEncoder()
df['Gender_Encoded'] = le.fit_transform(df['Gender'])
df['Internet_Encoded'] = le.fit_transform(df['Internet_Access'])

feature_cols = [
    'Study_Hours', 'Attendance_Percent', 'Previous_Score',
    'Sleep_Hours', 'Practice_Tests', 'Tutoring_Sessions',
    'Gender_Encoded', 'Internet_Encoded'
]
X = df[feature_cols]
y = df['Final_Score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# STEP 4: MLflow Experiment Setup
# ============================================================
EXPERIMENT_NAME = "Student_Performance_Prediction_Exp9"
mlflow.set_experiment(EXPERIMENT_NAME)

# ============================================================
# STEP 5: Train Models with MLflow Tracking
# ============================================================
print("\n[STEP 4] Training models with MLflow tracking...")

models_config = {
    "Linear_Regression": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "params": {"model_type": "LinearRegression", "scaling": "StandardScaler"}
    },
    "Decision_Tree": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("model", DecisionTreeRegressor(max_depth=8, random_state=42))
        ]),
        "params": {"model_type": "DecisionTree", "max_depth": 8}
    },
    "Random_Forest": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
        ]),
        "params": {"model_type": "RandomForest", "n_estimators": 100}
    },
    "Gradient_Boosting": {
        "pipeline": Pipeline([
            ("scaler", StandardScaler()),
            ("model", GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
        ]),
        "params": {"model_type": "GradientBoosting", "n_estimators": 100, "lr": 0.1}
    }
}

results = []

for model_name, config in models_config.items():
    print(f"\n  Training {model_name}...")

    with mlflow.start_run(run_name=model_name):
        # Tags
        mlflow.set_tag("model", model_name)
        mlflow.set_tag("task", "regression")
        mlflow.set_tag("dataset", "Student_Performance")
        mlflow.set_tag("author", "Jay Student")
        mlflow.set_tag("experiment_no", "9")

        # Parameters
        params = config["params"].copy()
        params.update({
            "n_features": len(feature_cols),
            "n_train_samples": len(X_train),
            "n_test_samples": len(X_test),
            "test_size": 0.2,
            "random_state": 42
        })
        mlflow.log_params(params)

        # Train
        pipeline = config["pipeline"]
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_pred = np.clip(y_pred, 0, 100)  # Scores must be 0-100

        # Metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        # Cross validation
        cv = cross_val_score(
            pipeline, X_train, y_train,
            cv=5, scoring='r2', n_jobs=-1
        )
        cv_r2_mean = cv.mean()
        cv_r2_std = cv.std()

        # Log metrics
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("cv_r2_mean", cv_r2_mean)
        mlflow.log_metric("cv_r2_std", cv_r2_std)

        # Log dataset as artifact
        mlflow.log_artifact("student_performance.csv")
        mlflow.log_artifact("eda_plots.png")

        # Log model
        mlflow.sklearn.log_model(
            pipeline,
            artifact_path=f"model/{model_name}",
            registered_model_name=f"StudentPerf_{model_name}"
        )

        # Prediction plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        axes[0].scatter(y_test, y_pred, alpha=0.5, s=15, color='steelblue')
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect prediction')
        axes[0].set_xlabel("Actual Score")
        axes[0].set_ylabel("Predicted Score")
        axes[0].set_title(f"{model_name}: Actual vs Predicted")
        axes[0].legend()

        residuals = y_test - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.4, s=15)
        axes[1].axhline(0, color='red', linestyle='--')
        axes[1].set_xlabel("Predicted Score")
        axes[1].set_ylabel("Residuals")
        axes[1].set_title(f"{model_name}: Residuals")

        plt.suptitle(f"{model_name} | MAE={mae:.2f} | RMSE={rmse:.2f} | R²={r2:.4f}")
        plt.tight_layout()
        plt.savefig(f"{model_name}_results.png", dpi=100)
        mlflow.log_artifact(f"{model_name}_results.png")
        plt.close()

        print(f"    MAE:  {mae:.4f}")
        print(f"    RMSE: {rmse:.4f}")
        print(f"    R²:   {r2:.4f}")
        print(f"    CV R² (mean±std): {cv_r2_mean:.4f} ± {cv_r2_std:.4f}")

        results.append({
            "Model": model_name,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2_Score": round(r2, 4),
            "CV_R2_Mean": round(cv_r2_mean, 4)
        })

# ============================================================
# STEP 6: Hyperparameter Tuning (Best Model)
# ============================================================
print("\n[STEP 5] Hyperparameter Tuning (Random Forest)...")

with mlflow.start_run(run_name="RF_HyperparamTuning"):
    mlflow.set_tag("type", "hyperparameter_tuning")
    mlflow.set_tag("base_model", "RandomForest")

    param_grid = {
        'model__n_estimators': [50, 100, 200],
        'model__max_depth': [5, 10, None],
        'model__min_samples_split': [2, 5]
    }

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(random_state=42, n_jobs=-1))
    ])

    grid_search = GridSearchCV(
        pipeline, param_grid, cv=3,
        scoring='r2', n_jobs=-1, verbose=0
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    y_pred_tuned = np.clip(best_model.predict(X_test), 0, 100)

    tuned_r2 = r2_score(y_test, y_pred_tuned)
    tuned_mae = mean_absolute_error(y_test, y_pred_tuned)
    tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred_tuned))

    mlflow.log_params(grid_search.best_params_)
    mlflow.log_metric("tuned_r2", tuned_r2)
    mlflow.log_metric("tuned_mae", tuned_mae)
    mlflow.log_metric("tuned_rmse", tuned_rmse)
    mlflow.sklearn.log_model(
        best_model,
        "tuned_rf_model",
        registered_model_name="StudentPerf_BestModel"
    )

    print(f"  Best params: {grid_search.best_params_}")
    print(f"  Tuned R²:   {tuned_r2:.4f}")
    print(f"  Tuned MAE:  {tuned_mae:.4f}")

# ============================================================
# STEP 7: Final Summary
# ============================================================
print("\n[STEP 6] Results Summary:")
results_df = pd.DataFrame(results).sort_values("R2_Score", ascending=False)
print(results_df.to_string(index=False))

with mlflow.start_run(run_name="Experiment9_Summary"):
    mlflow.set_tag("type", "final_summary")
    best = results_df.iloc[0]
    mlflow.log_param("best_model", best["Model"])
    mlflow.log_metric("best_r2", best["R2_Score"])
    mlflow.log_metric("best_mae", best["MAE"])

    results_df.to_csv("exp9_results.csv", index=False)
    mlflow.log_artifact("exp9_results.csv")

    # Final comparison chart
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336']

    for ax, metric in zip(axes, ['R2_Score', 'MAE', 'RMSE']):
        ascending = metric != 'R2_Score'
        sorted_df = results_df.sort_values(metric, ascending=ascending)
        bars = ax.bar(sorted_df['Model'], sorted_df[metric], color=colors)
        ax.set_title(f'{metric} Comparison')
        ax.set_ylabel(metric)
        plt.setp(ax.get_xticklabels(), rotation=15, ha='right')
        for bar, val in zip(bars, sorted_df[metric]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                   f'{val:.3f}', ha='center', va='bottom', fontsize=8)

    plt.suptitle('Experiment 9: Student Performance - Model Comparison', fontsize=13)
    plt.tight_layout()
    plt.savefig("exp9_final_comparison.png", dpi=100)
    mlflow.log_artifact("exp9_final_comparison.png")
    plt.close()

print("\n" + "="*60)
print(f"  Best Model: {results_df.iloc[0]['Model']}")
print(f"  Best R²: {results_df.iloc[0]['R2_Score']:.4f}")
print(f"  Best MAE: {results_df.iloc[0]['MAE']:.4f}")
print("="*60)
print("\nExperiment 9 Complete!")
print("View in MLflow UI: mlflow ui → http://localhost:5000")

# ============================================================
# STEP 8: Demonstrate Model Prediction
# ============================================================
print("\n[STEP 7] Predicting for a new student:")
new_student = pd.DataFrame({
    'Study_Hours': [7.5],
    'Attendance_Percent': [90.0],
    'Previous_Score': [78.0],
    'Sleep_Hours': [7.0],
    'Practice_Tests': [8],
    'Tutoring_Sessions': [4],
    'Gender_Encoded': [1],  # Female
    'Internet_Encoded': [1]  # Yes
})

best_pipeline = models_config["Random_Forest"]["pipeline"]
predicted_score = float(np.clip(best_pipeline.predict(new_student)[0], 0, 100))
print(f"  Student Profile: Study=7.5h, Attendance=90%, PrevScore=78, Sleep=7h")
print(f"  Predicted Final Score: {predicted_score:.2f}/100")
