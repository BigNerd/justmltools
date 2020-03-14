import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List

from justmltools.experiment.abstract_config import AbstractConfig


def mocked_json_load(stream: Any) -> Dict:
    return {"test_name": "test_value"}


class MyConcreteTestConfig(AbstractConfig):

    def __init__(self):
        config_dict: Dict = self._read_config_json_file(os.path.realpath(__file__))
        self.__test_name = config_dict["test_name"]

    @property
    def test_name(self):
        return self.__test_name


class TestAbstractConfig(TestCase):

    @patch('json.load', side_effect=mocked_json_load)
    def test_properties(self, os_listdir_function_mock: MagicMock):
        self.sut = MyConcreteTestConfig()
        properties: Dict = self.sut.properties()
        self.assertDictEqual(properties, mocked_json_load(None))

    @patch('json.load', side_effect=mocked_json_load)
    def test_property_names(self, os_listdir_function_mock: MagicMock):
        self.sut = MyConcreteTestConfig()
        property_names: List[str] = self.sut.property_names()
        self.assertListEqual(property_names, ["test_name"])
