from typing import List, Optional
from justmltools.config.abstract_data_path_config import AbstractDataPathConfig


class GitlabDataPathConfig(AbstractDataPathConfig):
    """ This class provides a Gitlab repo path layout
        for all input and output of transform, train and eval processes.
    """

    def __init__(self, prefix: Optional[str] = None):
        if prefix is not None:
            prefix = prefix.rstrip("/")
        super().__init__(prefix=prefix)

    def _join_segments(self, segments: List[str]) -> str:
        return "/".join(segments)
