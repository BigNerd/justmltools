from unittest import TestCase
from unittest.mock import Mock, patch
from mlflow.entities import RunData, Param
from typing import Any, Dict

from justmltools.repo.mlflow_repo_downloader import MlflowRepoDownloader
from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.mlflow_data_path_config import MlflowDataPathConfig


class TestMlflowRepoDownloader(TestCase):

    def create_downloader(self, run_id: str) -> MlflowRepoDownloader:
        downloader: MlflowRepoDownloader = MlflowRepoDownloader(
            local_data_path_config=LocalDataPathConfig(prefix="my_local_test_prefix"),
            remote_data_path_config=MlflowDataPathConfig(),
            aws_credentials=Mock(),
            experiment_name="my_test_experiment",
            run_id=run_id
        )
        return downloader

    def test_find_or_download_input_config_object(self):
        run_id: str = "my_test_run_id"
        sut: MlflowRepoDownloader = self.create_downloader(run_id)
        self.assertEqual(run_id, sut.resolved_run_id)

    def test_find_or_download_params(self):
        run_id: str = "my_test_run_id"
        sut: MlflowRepoDownloader = self.create_downloader(run_id)
        params = [ Param(key="test_param", value="test_param_value") ]
        run_data: RunData = RunData(metrics=None, params=params, tags=None)
        with patch.object(sut, '_MlflowRepoDownloader__get_run_data', return_value=run_data) as method:
            run_params: Dict[str, Any] = sut.find_or_download_run_params()
            self.assertEqual("test_param_value", run_params["test_param"])
