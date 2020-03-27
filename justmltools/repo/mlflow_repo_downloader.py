import mlflow.tracking as ml
from mlflow.tracking.client import MlflowClient
from mlflow.entities import Experiment, Run, RunData, RunInfo, ViewType
from functools import lru_cache
from typing import Any, Dict, List, Optional

from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.mlflow_data_path_config import MlflowDataPathConfig
from justmltools.repo.abstract_repo_downloader import AbstractRepoDownloader
from justmltools.s3.aws_credentials import AwsCredentials


class MlflowRepoDownloader(AbstractRepoDownloader):

    def __init__(
            self,
            local_data_path_config: LocalDataPathConfig,
            remote_data_path_config: MlflowDataPathConfig,
            aws_credentials: AwsCredentials,
            experiment_name: str,
            run_id: str):
        super().__init__(local_data_path_config=local_data_path_config, remote_data_path_config=remote_data_path_config)
        self.__aws_credentials = aws_credentials
        self.__experiment_name = experiment_name
        self.__run_id = run_id
        self.__resolved_run_id = None

    @property
    def resolved_run_id(self):
        if self.__resolved_run_id is None:
            self.__resolved_run_id = self.__resolve_run_id(self.__run_id)
        return self.__resolved_run_id

    def find_or_download_run_metrics(self) -> Dict[str, Any]:
        run_data: RunData = self.__get_run_data()
        return run_data.metrics

    def find_or_download_run_params(self) -> Dict[str, Any]:
        run_data: RunData = self.__get_run_data()
        return run_data.params

    def find_or_download_run_tags(self) -> Dict[str, Any]:
        run_data: RunData = self.__get_run_data()
        return run_data.tags

    def _download_object(self, remote_path: str, target_path: str):
        client: MlflowClient = self.__get_mlflow_client()
        dst_path: str = self._local_data_path_config.get_prefix()
        client.download_artifacts(
            run_id=self.resolved_run_id,
            path=remote_path,
            dst_path=dst_path
        )

    @lru_cache(maxsize=1)
    def __get_run_data(self) -> RunData:
        client: MlflowClient = self.__get_mlflow_client()
        run: Run = client.get_run(run_id=self.resolved_run_id)
        run_data: RunData = run.data
        return run_data

    def __resolve_run_id(self, run_id: str) -> str:
        """ maps the special run_id "latest" to a concrete id, returns all others as is
        :param run_id: "latest" or a valid MLflow run id of the experiment
        :return: the currently latest concrete run_id or the run_id as passed in
        """
        if run_id != "latest":
            return run_id  # leave as is
        client: MlflowClient = self.__get_mlflow_client()
        experiment: Experiment = client.get_experiment_by_name(self.__experiment_name)
        experiment_id: str = experiment.experiment_id
        run_infos: List[RunInfo] = \
            client.list_run_infos(experiment_id=experiment_id, run_view_type=ViewType.ACTIVE_ONLY)
        latest_start_time = 0
        latest_run_info: Optional[RunInfo] = None
        for run_info in run_infos:
            if run_info.start_time > latest_start_time:
                latest_start_time = run_info.start_time
                latest_run_info = run_info
        if latest_run_info is None:
            raise ValueError(f"no latest active run info found for experiment {self.__experiment_name}")
        return latest_run_info.run_id

    @lru_cache(maxsize=1)
    def __get_mlflow_client(self) -> MlflowClient:
        client: MlflowClient = ml.MlflowClient()
        return client
