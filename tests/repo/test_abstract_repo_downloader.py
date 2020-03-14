import os
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from justmltools.repo.abstract_repo_downloader import AbstractRepoDownloader
from justmltools.config.local_data_path_config import LocalDataPathConfig


def mocked_os_path_exists_unzipped(path: str) -> bool:
    return "exists" in path and ".zip" not in path


def mocked_os_path_exists_zipped(path: str) -> bool:
    return "exists" in path and ".zip" in path


class MyConcreteTestRepoDownloader(AbstractRepoDownloader):

    def _download_object(self, remote_path: str, target_path: str):
        if "exists" in target_path:
            raise FileExistsError()


class TestAbstractRepoDownloader(TestCase):

    @patch('os.path.exists', side_effect=mocked_os_path_exists_unzipped)
    def test_find_existing(self, os_path_exists_function: MagicMock):
        sut = MyConcreteTestRepoDownloader(
            remote_data_path_config=LocalDataPathConfig(prefix="test_prefix"),
            local_data_path_config=LocalDataPathConfig(prefix="test_prefix"))
        actual_path: str = sut.find_or_download_input_config_object(name_segments=["my_config_exists.json"])
        expected_path = os.path.join("test_prefix", "input", "config", "my_config_exists.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_input_data_object(name_segments=["my_data_exists.json"])
        expected_path = os.path.join("test_prefix", "input", "data", "my_data_exists.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_model_object(name_segments=["my_model_exists.json"])
        expected_path = os.path.join("test_prefix", "model", "my_model_exists.json")
        self.assertEqual(expected_path, actual_path)

    @patch.object(AbstractRepoDownloader, "_AbstractRepoDownloader__unzip_file")
    @patch('os.path.exists', side_effect=mocked_os_path_exists_zipped)
    def test_find_existing_zip(self, os_path_exists_function: MagicMock, zip_method: MagicMock):
        sut = MyConcreteTestRepoDownloader(
            remote_data_path_config=LocalDataPathConfig(prefix="test_prefix"),
            local_data_path_config=LocalDataPathConfig(prefix="test_prefix"))
        actual_path: str = sut.find_or_download_input_config_object(name_segments=["my_config_exists.json.zip"])
        expected_path = os.path.join("test_prefix", "input", "config", "my_config_exists.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_input_data_object(name_segments=["my_data_exists.json.zip"])
        expected_path = os.path.join("test_prefix", "input", "data", "my_data_exists.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_model_object(name_segments=["my_model_exists.json.zip"])
        expected_path = os.path.join("test_prefix", "model", "my_model_exists.json")
        self.assertEqual(expected_path, actual_path)

        self.assertEqual(3, zip_method.call_count)

    @patch.object(MyConcreteTestRepoDownloader, "_download_object")
    @patch.object(AbstractRepoDownloader, "_AbstractRepoDownloader__unzip_file")
    @patch('os.path.exists', side_effect=mocked_os_path_exists_unzipped)
    def test_download_non_existing(
            self, os_path_exists_function: MagicMock, zip_method: MagicMock, download_method: MagicMock):
        sut = MyConcreteTestRepoDownloader(
            remote_data_path_config=LocalDataPathConfig(prefix="test_prefix"),
            local_data_path_config=LocalDataPathConfig(prefix="test_prefix"))
        actual_path: str = sut.find_or_download_input_config_object(name_segments=["my_non_existing_config.json.zip"])
        expected_path = os.path.join("test_prefix", "input", "config", "my_non_existing_config.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_input_data_object(name_segments=["my_non_existing_data.json.zip"])
        expected_path = os.path.join("test_prefix", "input", "data", "my_non_existing_data.json")
        self.assertEqual(expected_path, actual_path)

        actual_path: str = sut.find_or_download_model_object(name_segments=["my_non_existing_model.json.zip"])
        expected_path = os.path.join("test_prefix", "model", "my_non_existing_model.json")
        self.assertEqual(expected_path, actual_path)

        self.assertEqual(3, zip_method.call_count)
        self.assertEqual(3, download_method.call_count)
