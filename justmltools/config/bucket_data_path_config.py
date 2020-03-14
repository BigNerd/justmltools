from typing import List
from justmltools.config.abstract_data_path_config import AbstractDataPathConfig


class BucketDataPathConfig(AbstractDataPathConfig):
    """ This class provides an S3 bucket path layout
        for all input and output of transform, train and eval processes.
    """

    def __init__(self, prefix: str):
        super().__init__(prefix=prefix.rstrip("/"))

    def _join_segments(self, segments: List[str]) -> str:
        return "/".join(segments)
