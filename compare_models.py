import mlflow
import mlflow.sklearn as sklearn_mlflow
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# --------------------------------------------------
# MLflow setup
# --------------------------------------------------

mlflow.set_experiment("MLFlow-Test")

# Automatically log parameters, metrics, model, etc.
sklearn_mlflow.autolog()


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

X, y = datasets.load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# --------------------------------------------------
# Define models
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        solver="lbfgs", max_iter=1000, random_state=8888
    ),
    "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=8888),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=8888
    ),
    "SVM": SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=8888),  # pyright: ignore[reportArgumentType]
}


# --------------------------------------------------
# Train and evaluate each model
# --------------------------------------------------

for model_name, model in models.items():
    print(f"\n{'=' * 50}")
    print(f"Training: {model_name}")
    print(f"{'=' * 50}")

    with mlflow.start_run(run_name=model_name):
        # Log the model name ourselves
        mlflow.log_param("model_name", model_name)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Metrics
        accuracy = float(accuracy_score(y_test, y_pred))
        precision = float(precision_score(y_test, y_pred, average="weighted"))
        recall = float(recall_score(y_test, y_pred, average="weighted"))
        f1 = float(f1_score(y_test, y_pred, average="weighted"))

        # Explicitly log metrics
        mlflow.log_metric("test_accuracy", accuracy)
        mlflow.log_metric("test_precision", precision)
        mlflow.log_metric("test_recall", recall)
        mlflow.log_metric("test_f1", f1)

        # Print results
        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
