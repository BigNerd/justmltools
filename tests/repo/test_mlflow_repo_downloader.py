from unittest import TestCase
from unittest.mock import Mock

from justmltools.repo.mlflow_repo_downloader import MlflowRepoDownloader
from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.mlflow_data_path_config import MlflowDataPathConfig


class TestMlflowRepoDownloader(TestCase):

    def test_find_or_download_input_config_object(self):
        _ = MlflowRepoDownloader(
            local_data_path_config=LocalDataPathConfig(prefix="my_local_test_prefix"),
            remote_data_path_config=MlflowDataPathConfig(),
            aws_credentials=Mock(),
            experiment_name="my_test_experiment",
            run_id="my_test_run_id"
        )
