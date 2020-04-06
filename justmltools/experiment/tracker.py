import mlflow
import os
import shutil

from typing import Any, Dict, List, Optional
from os.path import basename, dirname, sep


class Tracker:

    def __init__(self, experiment_name: str, artifact_root_path: str):
        self.__experiment_name: str = experiment_name
        self.__artifact_root_path: str = artifact_root_path

    def start_run(self):
        mlflow.set_experiment(self.__experiment_name)
        mlflow.start_run()

    def track(self,
              artifact_file_paths: Optional[List[str]] = None,
              parameters: Optional[Dict[str, Any]] = None,
              metrics: Optional[Dict[str, Any]] = None,
              tags: Optional[Dict[str, str]] = None):
        if artifact_file_paths:
            self.__track_artifacts(artifact_file_paths=artifact_file_paths)
        if parameters:
            for parameter_name, parameter_value in parameters.items():
                mlflow.log_param(parameter_name, parameter_value)
        if metrics:
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
        if tags:
            for tag_name, tag_value in tags.items():
                mlflow.set_tag(tag_name, tag_value)

    def __track_artifacts(self, artifact_file_paths: List[str]):
        for artifact_file_path in artifact_file_paths:
            if os.path.isdir(artifact_file_path):
                artifact_file_path = self.__zip_dir(dir_path=artifact_file_path)
            self.__track_artifact_file(artifact_file_path)

    def __track_artifact_file(self, artifact_file_path: str):
        mlflow_artifact_path: str = \
            artifact_file_path[len(self.__artifact_root_path):-len(basename(artifact_file_path))]
        mlflow_artifact_path = mlflow_artifact_path.strip(sep)  # remove leading and trailing / or \
        if self.__mlflow_repo_is_remote():
            mlflow_artifact_path = mlflow_artifact_path.replace(sep, "/")  # replace Windows separator with S3 slash
        mlflow.log_artifact(local_path=artifact_file_path, artifact_path=mlflow_artifact_path)

    @staticmethod
    def __zip_dir(dir_path: str) -> str:
        shutil.make_archive(base_name=dir_path, format="zip", root_dir=dirname(dir_path), base_dir=basename(dir_path))
        return dir_path + ".zip"

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
