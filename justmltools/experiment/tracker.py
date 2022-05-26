import mlflow
import os
import shutil

from typing import Any, Dict, List, Optional
from os.path import basename, dirname, sep


class Metric:
    """ Metric enables you to collect multiple values of a step dependent metric in your metrics dictionary;
        if your metric is not step dependent, you still can but need not use this class
        in order to track your single metric value
    """
    def __init__(self, key: str, value, step: Optional[int]):
        self.key = key
        self.value = value
        self.step = step


class Tracker:
    """
    Tracker is a simple facade to the MLflow API;

    You can use it one of two ways:
    a) using the with statement syntax (recommended for better readability thanks to indentation)
    ---------------------------------------------------------------------------------------------
    with Tracker(experiment_name="...", artifact_root_path="...") as tracker:
        run_id = tracker.get_active_run_id()
        ...
        tracker.track(...)
        ...

    b) using explicit calls to start_run and end_run:
    ---------------------------------------------------------------------------------------------
    tracker = Tracker(experiment_name="...", artifact_root_path="...")
    run_id = tracker.start_run()
    ...
    tracker.track(...)
    ...
    tracker.end_run()
    """

    def __init__(self, experiment_name: str, artifact_root_path: str):
        self.__experiment_name: str = experiment_name
        self.__artifact_root_path: str = artifact_root_path

    def __enter__(self):
        self.start_run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_run()
        return False

    def start_run(self) -> str:
        """ returns the active run id """
        mlflow.set_experiment(self.__experiment_name)
        mlflow.start_run()
        run_id = self.get_active_run_id()
        return run_id

    def track(self,
              artifact_file_paths: Optional[List[str]] = None,
              parameters: Optional[Dict[str, Any]] = None,
              metrics: Optional[Dict[str, Any]] = None,
              tags: Optional[Dict[str, str]] = None,
              note: Optional[str] = None,
    ):
        if artifact_file_paths:
            self.track_artifacts(artifact_file_paths=artifact_file_paths)
        if parameters:
            for parameter_name, parameter_value in parameters.items():
                mlflow.log_param(parameter_name, parameter_value)
        if metrics:
            for metric_name, metric_value in metrics.items():
                if isinstance(metric_value, Metric):
                    step: int = 0
                    if metric_value.step is not None:
                        step = metric_value.step
                    mlflow.log_metric(key=metric_value.key, value=metric_value.value, step=step)
                else:
                    mlflow.log_metric(metric_name, metric_value)
        if tags:
            for tag_name, tag_value in tags.items():
                mlflow.set_tag(tag_name, tag_value)
        if note:
            mlflow.set_tag("mlflow.note.content", note)

    def track_artifacts(self, artifact_file_paths: List[str]):
        for artifact_file_path in artifact_file_paths:
            if os.path.isdir(artifact_file_path):
                artifact_file_path = self.__zip_dir(dir_path=artifact_file_path)
            self.track_artifact_file(artifact_file_path)

    def track_artifact_file(self, artifact_file_path: str, mlflow_artifact_dir_path: Optional[str] = None) -> str:
        """
        :param artifact_file_path: Local path to the file to write.
        :param mlflow_artifact_dir_path: If provided, the directory in ``artifact_uri`` to write to.
                                     If not provided, the directory will be derived
        :return: the MLflow artifact file path
        """
        if mlflow_artifact_dir_path is None:
            if artifact_file_path.startswith(self.__artifact_root_path):
                mlflow_artifact_dir_path: str = \
                    artifact_file_path[len(self.__artifact_root_path):-len(basename(artifact_file_path))]
            else:
                mlflow_artifact_dir_path = ""
        mlflow_artifact_dir_path = mlflow_artifact_dir_path.strip(sep)  # remove leading and trailing / or \
        if self.__mlflow_repo_is_remote():
            # replace local (e.g. Windows) separator with S3 slash
            mlflow_artifact_dir_path = mlflow_artifact_dir_path.replace(sep, "/")
        mlflow.log_artifact(local_path=artifact_file_path, artifact_path=mlflow_artifact_dir_path)
        if len(mlflow_artifact_dir_path) > 0:
            mlflow_artifact_file_path = f"{mlflow_artifact_dir_path}/{basename(artifact_file_path)}"
        else:
            mlflow_artifact_file_path = basename(artifact_file_path)
        return mlflow_artifact_file_path

    @staticmethod
    def get_artifact_uri(mlflow_artifact_file_path: str) -> str:
        uri: str = mlflow.get_artifact_uri(artifact_path=mlflow_artifact_file_path)
        return uri

    @staticmethod
    def __zip_dir(dir_path: str) -> str:
        shutil.make_archive(base_name=dir_path, format="zip", root_dir=dirname(dir_path), base_dir=basename(dir_path))
        return dir_path + ".zip"

    @staticmethod
    def get_active_run_id() -> str:
        """ returns the mlflow active run id or an empty string """
        active_run = mlflow.active_run()
        run_id = ""
        if active_run is not None:
            run_id = active_run.info.run_id
        return run_id

    @staticmethod
    def end_run():
        mlflow.end_run()

    @staticmethod
    def __mlflow_repo_is_remote() -> bool:
        result: bool = False
        env_name = "MLFLOW_TRACKING_URI"
        if env_name in os.environ:
            env_value = os.environ[env_name]
            result = "localhost" not in env_value
        return result
