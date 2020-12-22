import os
from inflection import underscore
from pathlib import Path
from typing import List

from gen.class_info import ClassInfo
from gen.parser import Parser


class TestGenerator:

    def generate(
            self,
            package_name: str,
            src_dir_path: str,
            excluded_classes=()):
        parsed_modules: List[ClassInfo] = Parser().parse_package(package_name, src_dir_path)
        for class_info in parsed_modules:
            if class_info.class_name is None or \
                    class_info.class_name in excluded_classes:
                continue  # skip generating a test for a class which is special
            target_dir_path: str = os.path.join(
                src_dir_path,
                ("tests" + package_name[package_name.index("."):]).replace(".", os.path.sep)
            )
            target_file_path: str = os.path.join(
                target_dir_path,
                "test_" + class_info.module_name + ".py")
            if os.path.exists(target_file_path):
                continue  # skip generating a test which already exists
            Path(target_dir_path).mkdir(parents=True, exist_ok=True)
            self.__generate_test_file(target_file_path, class_info)

    def __generate_test_file(self, target_file_path: str, class_info: ClassInfo):
        def excluded_from_style_import(from_style_import: str) -> bool:
            excluded_prefixes = ['typing.']
            for excluded_prefix in excluded_prefixes:
                if from_style_import.startswith(excluded_prefix):
                    return True
            return False
        from_style_imports = [from_style_import for from_style_import in class_info.from_style_imports
                              if not excluded_from_style_import(from_style_import)]
        with open(target_file_path, "w") as file:
            file.write("from unittest import TestCase\n")
            file.write("from unittest.mock import MagicMock, patch\n")
            file.write("\n" * 2)
            file.write(f"class Test{class_info.class_name}(TestCase):\n")
            file.write("\n")
            for public_method in class_info.public_methods:
                for from_style_import in from_style_imports:
                    file.write(f"    @patch('{from_style_import}')\n")
                file.write(f"    def test_{public_method}(\n")
                file.write(f"        self,\n")
                for from_style_import in reversed(from_style_imports):
                    param_name = underscore(from_style_import.split(".")[-1]) + "_mock"
                    file.write(f"        {param_name}: MagicMock,\n")
                file.write(f"    ):\n")
                import_sut = f"from {class_info.package_name}.{class_info.module_name} import {class_info.class_name}"
                file.write(f"        {import_sut}\n")
                file.write(f"        self.skipTest(\"not implemented yet\")\n")
                file.write("\n")


if __name__ == '__main__':
    src_dir_path = os.path.join(os.path.dirname(__file__), "..")
    generator: TestGenerator = TestGenerator()
    for short_package_name in ("config", "experiment", "repo", "s3"):
        generator.generate(
            src_dir_path=src_dir_path,
            package_name=f"justmltools.{short_package_name}",
            excluded_classes=[]
        )
