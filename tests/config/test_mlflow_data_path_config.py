from unittest import TestCase

from justmltools.config.mlflow_data_path_config import MlflowDataPathConfig

PREFIX = None


class TestMlflowDataPathConfig(TestCase):

    def setUp(self) -> None:
        self.sut: MlflowDataPathConfig = MlflowDataPathConfig()

    def test_get_prefix(self):
        self.assertEqual(PREFIX, self.sut.get_prefix())

    def test_get_input_config_path(self):
        self.assertEqual(f"input/config", self.sut.get_input_config_path())

    def test_get_input_data_path(self):
        self.assertEqual(f"input/data", self.sut.get_input_data_path())

    def test_get_model_path(self):
        self.assertEqual(f"model", self.sut.get_model_path())

    def test_get_output_path(self):
        self.assertEqual(f"output", self.sut.get_output_path())

    def test_join_one_more_level(self):
        joined_path: str = self.sut.join(self.sut.get_output_path(), "my_file")
        self.assertEqual(f"output/my_file", joined_path)

    def test_join_two_more_levels(self):
        joined_path: str = self.sut.join(self.sut.get_output_path(), ["my_sub_dir", "my_file"])
        self.assertEqual(f"output/my_sub_dir/my_file", joined_path)