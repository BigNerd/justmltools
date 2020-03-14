import os
from typing import List
from justmltools.config.abstract_data_path_config import AbstractDataPathConfig


class LocalDataPathConfig(AbstractDataPathConfig):
    """ This class provides the local file system path layout
        for all input and output of transform, train and eval processes.
    """

    def __init__(self, prefix: str):
        super().__init__(prefix=prefix.rstrip(os.path.sep))

    def _join_segments(self, segments: List[str]) -> str:
        return os.path.join(*segments)
