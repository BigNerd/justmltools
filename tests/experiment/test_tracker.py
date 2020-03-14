from unittest import TestCase
from unittest.mock import MagicMock, patch

from justmltools.experiment.tracker import Tracker


def mocked_mlflow_set_experiment(experiment_name: str):
    pass


def mocked_mlflow_log_artifact(local_path: str, artifact_path: str):
    pass


def mocked_mlflow_log_param(param_name: str, param_value):
    pass


def mocked_mlflow_log_metric(metric_name: str, metric_value):
    pass


def mocked_mlflow_set_tag(tag_name: str, tag_value):
    pass


def mocked_mlflow_end_run():
    pass


class TestTracker(TestCase):

    @patch('mlflow.set_experiment', side_effect=mocked_mlflow_set_experiment)
    @patch('mlflow.log_artifact', side_effect=mocked_mlflow_log_artifact)
    @patch('mlflow.log_param', side_effect=mocked_mlflow_log_param)
    @patch('mlflow.log_metric', side_effect=mocked_mlflow_log_metric)
    @patch('mlflow.set_tag', side_effect=mocked_mlflow_set_tag)
    @patch('mlflow.end_run', side_effect=mocked_mlflow_end_run)
    def test_(self,
              mlflow_set_experiment_mock: MagicMock,
              mlflow_log_artifact_mock: MagicMock,
              mlflow_log_param_mock: MagicMock,
              mlflow_log_metric_mock: MagicMock,
              mlflow_set_tag_mock: MagicMock,
              mlflow_end_run_mock: MagicMock):
        self.sut: Tracker = Tracker(experiment_name="my_test_experiment", artifact_root_path="path_to_my_artifacts")
        self.sut.start_run()
        # perform the actual experiment collecting data to track... and then data over to the tracker
        self.sut.track(
            artifact_file_paths=["my_artifact_path_1", "my_artifact_path_2"],
            parameters={},
            metrics={},
            tags={}
        )
        self.sut.end_run()
