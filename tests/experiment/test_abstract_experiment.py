import os
from unittest import TestCase
from unittest.mock import Mock

from justmltools.repo.bucket_repo_downloader import BucketRepoDownloader
from justmltools.repo.mlflow_repo_downloader import MlflowRepoDownloader
from justmltools.experiment.abstract_experiment import AbstractExperiment


class MyConcreteTestExperiment(AbstractExperiment):

    def __init__(self):
        super().__init__(project_name="my_test_project")
        os.environ["DATA_DIR"] = os.getcwd()

    def _get_bucket_repo_downloader(self) -> BucketRepoDownloader:
        return BucketRepoDownloader(
            local_data_path_config=self._get_local_data_path_config(),
            remote_data_path_config=self._get_bucket_data_path_config(),
            bucket="my_bucket",
            aws_credentials=Mock()
        )

    def _get_mlflow_repo_downloader(self, experiment_name: str, run_id: str) -> MlflowRepoDownloader:
        return MlflowRepoDownloader(
            local_data_path_config=self._get_local_data_path_config(),
            remote_data_path_config=self._get_mlflow_data_path_config(),
            aws_credentials=Mock(),
            experiment_name="my_test_experiment",
            run_id="my_test_run_id"
        )

    def run(self):
        _: BucketRepoDownloader = self._get_bucket_repo_downloader()
        _: MlflowRepoDownloader = self._get_mlflow_repo_downloader(experiment_name="e", run_id="r")
        # use downloaders to find or download (and possibly unzip) file needed for the experiment


class TestAbstractExperiment(TestCase):

    def test_properties(self):
        sut: MyConcreteTestExperiment = MyConcreteTestExperiment()
        self.assertIsInstance(sut, AbstractExperiment)
        sut.run()
