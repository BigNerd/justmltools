import abc
from typing import List, Optional, Union


class AbstractDataPathConfig(abc.ABC):
    """ This class provides the abstract path layout
        for all input and output of transform, train and eval processes.
        Concrete implementation can vary in their path prefixes and the way path segments are joined as full paths
    """

    def __init__(self, prefix: Optional[str]):
        self._prefix = prefix

    def get_prefix(self):
        return self._prefix

    def get_input_config_path(self):
        return self._join_segments(self._get_input_config_segments())

    def get_input_data_path(self):
        return self._join_segments(self._get_input_data_segments())

    def get_model_path(self):
        return self._join_segments(self._get_model_segments())

    def get_output_path(self):
        return self._join_segments(self._get_output_segments())

    def join(self, path: str, segments: Union[str, List[str]]) -> str:
        if isinstance(segments, str):
            segments: List[str] = [segments]
        segments.insert(0, path)
        return self._join_segments(segments)

    @abc.abstractmethod
    def _join_segments(self, segments: List[str]) -> str:
        pass

    def _get_input_config_segments(self) -> List[Optional[str]]:
        segments: List[Optional[str]] = [self.get_prefix(), "input", "config"]
        return self.__remove_none_segments(segments)

    def _get_input_data_segments(self) -> List[Optional[str]]:
        segments: List[Optional[str]] = [self.get_prefix(), "input", "data"]
        return self.__remove_none_segments(segments)

    def _get_model_segments(self) -> List[Optional[str]]:
        segments: List[Optional[str]] = [self.get_prefix(), "model"]
        return self.__remove_none_segments(segments)

    def _get_output_segments(self) -> List[Optional[str]]:
        segments: List[Optional[str]] = [self.get_prefix(), "output"]
        return self.__remove_none_segments(segments)

    @staticmethod
    def __remove_none_segments(segments: List[Optional[str]]) -> List[str]:
        return [s for s in segments if s]
