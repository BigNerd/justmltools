import os
from typing import List

from justmltools.gen.class_info import ClassInfo
from justmltools.gen.parser import Parser


class UmlGenerator:

    @staticmethod
    def generate(
             package_name: str,
             src_dir_path: str,
             target_file_path: str,
             excluded_classes=(),
             up_arrow_used_classes=(),
             up_arrow_super_classes=()):
        with open(target_file_path, "w") as file:
            file.write("@startuml\n")
            parsed_modules: List[ClassInfo] = Parser().parse_package(package_name, src_dir_path)
            parsed_modules.sort(key=lambda class_info: "" if class_info.class_name is None else class_info.class_name)
            for class_info in parsed_modules:
                if class_info.class_name is not None and class_info.class_name not in excluded_classes:
                    is_abstract_class = \
                        class_info.super_class_name is not None and class_info.super_class_name == "abc.ABC"
                    modifier = ""
                    if is_abstract_class:
                        modifier = "abstract "
                    file.write(f"{modifier}class {class_info.class_name}\n")
                    file.write("{\n")
                    for public_attribute in class_info.public_attributes:
                        file.write(f"  {public_attribute}\n")
                    for protected_attribute in class_info.protected_attributes:
                        file.write(f"  {protected_attribute}\n")
                    for public_method in class_info.public_methods:
                        file.write(f"  {public_method}()\n")
                    for protected_method in class_info.protected_methods:
                        file.write(f"  {protected_method}()\n")
                    file.write("}\n")
                    if class_info.super_class_name is not None and not is_abstract_class:
                        arrow = "--|>"
                        if class_info.super_class_name in up_arrow_super_classes:
                            arrow = "-up-|>"
                        file.write(f"{class_info.class_name} {arrow} {class_info.super_class_name}\n")
                    for used_class in class_info.used_classes:
                        if used_class not in excluded_classes and used_class != class_info.super_class_name:
                            arrow = "-->"
                            if used_class in up_arrow_used_classes:
                                arrow = "-up->"
                            file.write(f"{class_info.class_name} {arrow} {used_class}\n")
            file.write("@enduml\n")


if __name__ == '__main__':
    src_dir_path = os.path.join(os.path.dirname(__file__), "..", "..")
    target_dir_path = os.path.join(os.path.dirname(__file__), "..", "..", "doc", "plantuml")
    generator: UmlGenerator = UmlGenerator()
    for short_package_name in ("config", "experiment", "repo", "s3"):
        generator.generate(
            src_dir_path=src_dir_path,
            package_name=f"justmltools.{short_package_name}",
            target_file_path=os.path.join(target_dir_path, f"{short_package_name}_class_diagram.puml"),
            excluded_classes=[],
            up_arrow_used_classes=[],
            up_arrow_super_classes=[]
        )
