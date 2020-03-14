import abc
import inspect
import json
from typing import Any, Dict, List


class AbstractConfig(abc.ABC):

    def properties(self, enums_as_strings: bool = True) -> Dict[str, Any]:
        """
        :param enums_as_strings: whether to convert enum values to strings, default is True
        :return: a dictionary with all public properties of this object, useful for generic tracking with MLflow
        """
        properties = {}
        for name in self.property_names():
            value = getattr(self, name)
            if enums_as_strings and value is not None and hasattr(value, 'name'):
                properties[name] = value.name
            else:
                properties[name] = value
        return properties

    def property_names(self) -> List[str]:
        result: List[str] = []
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('_') and not inspect.ismethod(value):
                result.append(name)
        return result

    @staticmethod
    def _read_config_json_file(config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as stream:
            config_dict = json.load(stream)
        return config_dict
