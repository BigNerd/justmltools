import abc
import os
import pkg_resources

from typing import List, Optional
from justmltools.config.bucket_data_path_config import BucketDataPathConfig
from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.mlflow_data_path_config import MlflowDataPathConfig


class AbstractExperiment(abc.ABC):

    def __init__(self, project_name: str):
        self.__project_name = project_name

    def _get_local_data_path_config(self) -> LocalDataPathConfig:
        data_path_config = LocalDataPathConfig(
            prefix=self._get_file_system_prefix(),
        )
        return data_path_config

    def _get_bucket_data_path_config(self) -> BucketDataPathConfig:
        data_path_config = BucketDataPathConfig(
            prefix=self._get_bucket_prefix(),
        )
        return data_path_config

    @staticmethod
    def _get_mlflow_data_path_config() -> MlflowDataPathConfig:
        data_path_config = MlflowDataPathConfig()
        return data_path_config

    @staticmethod
    def _get_file_system_prefix() -> str:
        data_dir: str = "DATA_DIR"
        if data_dir not in os.environ:
            raise ValueError(f"environment variable {data_dir} is not set")
        file_system_prefix: str = os.environ["DATA_DIR"]
        if not os.path.isdir(file_system_prefix):
            raise ValueError(f"environment variable {data_dir}='{file_system_prefix}' defines an invalid directory")
        return file_system_prefix

    def _get_bucket_prefix(self) -> str:
        return f"projects/{self.__project_name}"

    @staticmethod
    def _get_installed_packages() -> List[str]:
        installed_packages = sorted([f"{i.key}=={i.version}" for i in pkg_resources.working_set])
        return installed_packages

    @staticmethod
    def _get_git_commit_hash() -> Optional[str]:
        git_commit_hash = os.environ.get("GIT_COMMIT_HASH")
        if git_commit_hash is not None and len(git_commit_hash) == 0:
            git_commit_hash = None
        return git_commit_hash
