
from pathlib import Path

import mlflow
import mlflow.sklearn as sklearn_mlflow
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# MLflow configuration
# --------------------------------------------------

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("MLFlow-Test")

# Enable automatic logging of parameters, metrics, and model.
sklearn_mlflow.autolog()


# --------------------------------------------------
# Load the Iris dataset
# --------------------------------------------------

X, y = datasets.load_iris(return_X_y=True)


# --------------------------------------------------
# Split the data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


# --------------------------------------------------
# Define model hyperparameters
# --------------------------------------------------

params: dict[str, str | int] = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "random_state": 8888,
}


# --------------------------------------------------
# Train the model
# --------------------------------------------------

lr = LogisticRegression(**params)

lr.fit(X_train, y_train)


# --------------------------------------------------
# Make predictions
# --------------------------------------------------

y_pred = lr.predict(X_test)


# --------------------------------------------------
# Calculate evaluation metrics
# --------------------------------------------------

accuracy = float(accuracy_score(y_test, y_pred))

precision = float(
    precision_score(
        y_test,
        y_pred,
        average="weighted",
    )
)

recall = float(
    recall_score(
        y_test,
        y_pred,
        average="weighted",
    )
)

f1 = float(
    f1_score(
        y_test,
        y_pred,
        average="weighted",
    )
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("Logistic Regression Results")
print("---------------------------")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
