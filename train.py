# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import warnings
import sys
import argparse
import yaml
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from mlflow.tracking import MlflowClient
from mlflow.tracking.fluent import _get_experiment_id
import mlflow
import mlflow.sklearn


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--alpha")
    # parser.add_argument("--l1-ratio")
    # args = parser.parse_args()

    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    wine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wine-quality.csv")
    data = pd.read_csv(wine_path)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    client = MlflowClient()
    exp_id = _get_experiment_id()
    experiment = client.get_experiment(exp_id)
    artifact_location = experiment.artifact_location
    exp_name = experiment.name
    if not artifact_location.startswith("./mlruns/"):
        path = f"./mlruns/{exp_id}/meta.yaml"
        with open(path) as file:
            documents = yaml.full_load(file)
        documents['artifact_location'] = f"file:./mlruns/{exp_id}"
        with open(path, 'w') as yamlfile:
            data = yaml.dump(documents, yamlfile)
    else:
        pass
    with mlflow.start_run() as run:
        run_id = run.run_id = run.info.run_uuid
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(lr, artifact_path='models')

    path_run = f"./mlruns/{exp_id}/{run_id}/meta.yaml"
    with open(path_run) as file:
        documents = yaml.full_load(file)
    artifact_uri = documents['artifact_uri']
    if not artifact_uri.startswith("./mlruns/"):
        documents['artifact_uri'] = f"./mlruns/{exp_id}/{run_id}/artifacts"
        with open(path_run, 'w') as yamlfile:
            data = yaml.dump(documents, yamlfile)
    else:
        pass
