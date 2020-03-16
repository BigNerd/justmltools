import abc
import os
import zipfile
from typing import List

from justmltools.config.abstract_data_path_config import AbstractDataPathConfig
from justmltools.config.local_data_path_config import LocalDataPathConfig


class AbstractRepoDownloader(abc.ABC):

    def __init__(self, remote_data_path_config: AbstractDataPathConfig, local_data_path_config: LocalDataPathConfig):
        self._remote_data_path_config = remote_data_path_config
        self._local_data_path_config = local_data_path_config

    def find_or_download_input_config_object(self, name_segments: List[str]) -> str:
        base_local_path: str = self._local_data_path_config.get_input_config_path()
        base_remote_path = self._remote_data_path_config.get_input_config_path()
        local_path: str = self.__find_or_download_object(
            base_local_path=base_local_path,
            base_remote_path=base_remote_path,
            additional_name_segments=name_segments
        )
        return local_path

    def find_or_download_input_data_object(self, name_segments: List[str]) -> str:
        base_local_path: str = self._local_data_path_config.get_input_data_path()
        base_remote_path = self._remote_data_path_config.get_input_data_path()
        local_path: str = self.__find_or_download_object(
            base_local_path=base_local_path,
            base_remote_path=base_remote_path,
            additional_name_segments=name_segments
        )
        return local_path

    def find_or_download_model_object(self, name_segments: List[str]) -> str:
        base_local_path: str = self._local_data_path_config.get_model_path()
        base_remote_path = self._remote_data_path_config.get_model_path()
        local_path: str = self.__find_or_download_object(
            base_local_path=base_local_path,
            base_remote_path=base_remote_path,
            additional_name_segments=name_segments
        )
        return local_path

    def __find_or_download_object(
            self, base_local_path: str, base_remote_path: str, additional_name_segments: List[str]) -> str:
        target_path: str = base_local_path
        for name_segment in additional_name_segments:
            target_path = os.path.join(target_path, name_segment)
        target_path_without_zip_extension: str = self.__remove_zip_extension(target_path)

        if os.path.exists(target_path_without_zip_extension):
            # unzipped file exists
            return target_path_without_zip_extension

        if target_path.endswith(".zip") and os.path.exists(target_path):
            # zipped file exists
            self.__unzip_file(zip_file_path=target_path)
            return target_path_without_zip_extension

        # download zipped or unzipped file from remote repo
        remote_path = base_remote_path
        for name_segment in additional_name_segments:
            remote_path = "/".join([remote_path, name_segment])
        self._download_object(remote_path=remote_path, target_path=target_path)
        if target_path.endswith(".zip"):
            self.__unzip_file(zip_file_path=target_path)
        return target_path_without_zip_extension

    @abc.abstractmethod
    def _download_object(self, remote_path: str, target_path: str):
        pass

    def __unzip_file(self, zip_file_path: str) -> str:
        assert(zip_file_path.endswith(".zip"))
        dir_path_to_unzip_to = os.path.dirname(os.path.abspath(zip_file_path))
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(dir_path_to_unzip_to)
        return self.__remove_zip_extension(path=zip_file_path)

    @staticmethod
    def __remove_zip_extension(path: str):
        if path.endswith(".zip"):
            path = path[:-len(".zip")]
        return path
