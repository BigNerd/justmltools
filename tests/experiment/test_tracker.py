from unittest import TestCase
from unittest.mock import MagicMock, patch

from justmltools.experiment.tracker import Tracker


def mocked_os_path_isdir(path: str) -> bool:
    return "dir" in path


def mocked_make_archive(base_name: str, format: str, root_dir: str, base_dir: str):
    pass


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

    @patch('mlflow.end_run', side_effect=mocked_mlflow_end_run)
    @patch('mlflow.set_tag', side_effect=mocked_mlflow_set_tag)
    @patch('mlflow.log_metric', side_effect=mocked_mlflow_log_metric)
    @patch('mlflow.log_param', side_effect=mocked_mlflow_log_param)
    @patch('mlflow.log_artifact', side_effect=mocked_mlflow_log_artifact)
    @patch('mlflow.set_experiment', side_effect=mocked_mlflow_set_experiment)
    @patch('shutil.make_archive', side_effect=mocked_make_archive)
    @patch('os.path.isdir', side_effect=mocked_os_path_isdir)
    def test_(self,
              os_path_isdir_mock: MagicMock,
              shutil_make_archive_mock: MagicMock,
              mlflow_set_experiment_mock: MagicMock,
              mlflow_log_artifact_mock: MagicMock,
              mlflow_log_param_mock: MagicMock,
              mlflow_log_metric_mock: MagicMock,
              mlflow_set_tag_mock: MagicMock,
              mlflow_end_run_mock: MagicMock):
        self.sut: Tracker = Tracker(experiment_name="my_test_experiment", artifact_root_path="path_to_my_artifacts")
        self.sut.start_run()
        mlflow_set_experiment_mock.assert_called_once()
        # perform the actual experiment collecting data to track... and then data over to the tracker
        self.sut.track(
            artifact_file_paths=["my_artifact_path_1", "my_artifact_path_2"],
            parameters={"my_param": "my_param_value"},
            metrics={"my_metric": 1.0},
            tags={"my_tag": "my_tag_value"}
        )
        mlflow_log_param_mock.assert_called()
        mlflow_log_metric_mock.assert_called()
        mlflow_set_tag_mock.assert_called()
        mlflow_log_artifact_mock.assert_called()
        os_path_isdir_mock.assert_called()
        shutil_make_archive_mock.assert_not_called()

        self.sut.track(
            artifact_file_paths=["my_artifact_path_1", "my_artifact_path_2", "my_artifact_dir_path"],
            parameters={},
            metrics={},
            tags={}
        )
        os_path_isdir_mock.assert_called()
        shutil_make_archive_mock.assert_called_once()

        self.sut.end_run()
        mlflow_end_run_mock.assert_called_once()
