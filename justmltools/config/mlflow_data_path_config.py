from typing import List
from justmltools.config.abstract_data_path_config import AbstractDataPathConfig


class MlflowDataPathConfig(AbstractDataPathConfig):
    """ This class provides an MLflow repo path layout
        for all input and output of transform, train and eval processes.
    """

    def __init__(self):
        super().__init__(prefix=None)

    def _join_segments(self, segments: List[str]) -> str:
        return "/".join(segments)
