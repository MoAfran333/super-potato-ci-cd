from typing import cast

import mlflow
import optuna
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

mlflow.set_experiment("Hyperparameter Tuning Experiment 2")

X, y = fetch_california_housing(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, random_state=0
)


def objective(trial):
    # Suggest hyperparameters
    rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32)
    rf_n_estimators = trial.suggest_int(
        "rf_n_estimators", 50, 300, step=10
    )
    rf_max_features = trial.suggest_float(
        "rf_max_features", 0.2, 1.0
    )

    params = {
        "max_depth": rf_max_depth,
        "n_estimators": rf_n_estimators,
        "max_features": rf_max_features,
    }

    # Create a child MLflow run for this trial
    with mlflow.start_run(
        nested=True,
        run_name=f"trial_{trial.number}"
    ) as child_run:

        # Log trial number
        mlflow.log_param("trial_number", trial.number)

        # Log hyperparameter values
        mlflow.log_params(params)

        # Train model
        regressor_obj = RandomForestRegressor(**params)
        regressor_obj.fit(X_train, y_train)

        # Predict and calculate error
        y_pred = regressor_obj.predict(X_val)
        error = mean_squared_error(y_val, y_pred)

        # Log trial metric
        mlflow.log_metric("error", error)

        # Log model
        mlflow.sklearn.log_model(
            regressor_obj,
            name="model"
        )

        # Store run ID for retrieving the best trial
        trial.set_user_attr(
            "run_id",
            child_run.info.run_id
        )

        # Print each trial's values
        print(f"\nTrial {trial.number}")
        print(f"Parameters: {params}")
        print(f"Error: {error}")
        print(f"Run ID: {child_run.info.run_id}")

        return error


# Parent run
with mlflow.start_run(run_name="study") as run:

    n_trials = 15

    mlflow.log_param("n_trials", n_trials)

    study = optuna.create_study(direction="minimize")

    study.optimize(objective, n_trials=n_trials)

    # Log best trial information
    mlflow.log_params(study.best_trial.params)
    mlflow.log_metric("best_error", study.best_value)

    if best_run_id := study.best_trial.user_attrs.get("run_id"):
        mlflow.log_param("best_child_run_id", best_run_id)

    # Print all trial values
    print("\n========== ALL TRIALS ==========")

    for trial in study.trials:
        print(
            f"Trial: {trial.number} | "
            f"Value: {trial.value} | "
            f"Params: {trial.params}"
        )

    print("\n========== BEST TRIAL ==========")
    print(f"Trial Number: {study.best_trial.number}")
    print(f"Best Value: {study.best_value}")
    print(f"Best Parameters: {study.best_trial.params}")