import sys
from mlflow.tracking import MlflowClient

exp_name = str(sys.argv[1]) if len(sys.argv) > 1 else "exp"
# run_name = str(sys.argv[2]) if len(sys.argv) > 2 else "unnamed"
client = MlflowClient()
exp_info = client.get_experiment_by_name(exp_name)
if exp_info:
    exp_id = exp_info.experiment_id
else:
    last_experiment_number = len(client.list_experiments())-1
    current_experiment_number = last_experiment_number + 1
    exp_id = exp_info.experiment_id if exp_info else MlflowClient().\
            create_experiment(exp_name, artifact_location= f"file:./mlruns/{current_experiment_number}")
