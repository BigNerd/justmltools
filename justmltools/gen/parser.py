import os
import re
from typing import List, Optional
from justmltools.gen.class_info import ClassInfo


class Parser:

    def parse_package(
            self, package_name: str, src_dir_path: str) -> List[ClassInfo]:
        package_path = os.path.join(src_dir_path, package_name.replace(".", os.path.sep))
        parsed_modules: List[ClassInfo] = []
        for module_file_name in os.listdir(package_path):
            if module_file_name.startswith("__"):
                continue
            else:
                module_path = os.path.join(package_path, module_file_name)
                module_name = module_file_name.replace(".py", "")
                class_info: ClassInfo = self.__parse_module(
                    package_name=package_name,
                    module_path=module_path,
                    module_name=module_name
                )
                parsed_modules.append(class_info)
        return parsed_modules

    @staticmethod
    def __parse_module(
            package_name: str,
            module_path: str,
            module_name: str) -> ClassInfo:
        class_name = None
        super_class_name = None
        used_classes = []
        public_attributes = []
        protected_attributes = []
        public_methods = []
        protected_methods = []
        with open(module_path, "r") as file:
            next_method_is_property = False
            while True:
                line: str = file.readline()
                if not line:
                    break

                match = re.match('from ' + package_name.replace(".", r"\.") + r'\.(.*) import ([A-Z].*)', line)
                if match is not None:
                    used_classes.append(match.group(2).split(",")[0])

                match = re.match(r'class (.*):.*', line)
                if match is not None:
                    class_name_with_super = match.group(1)
                    class_name_parts = class_name_with_super.split("(")
                    class_name = class_name_parts[0]
                    super_class_name = None  # reset in case it was detected as part of a previous class in this module
                    if len(class_name_parts) > 1 and len(class_name_parts[1]) > 0:
                        super_class_name = class_name_parts[1].rstrip(")")

                match = re.match(r'\s{4}@(arg|property)', line)
                if match is not None:
                    next_method_is_property = True

                match = re.match(r'\s{4}def ([^_].*)\(.*', line)
                if match is not None:
                    if next_method_is_property:
                        public_attributes.append(match.group(1).split("(")[0])
                        next_method_is_property = False
                    else:
                        public_methods.append(match.group(1).split("(")[0])

                match = re.match(r'\s{4}def (_[^_].*)\(.*', line)
                if match is not None:
                    if next_method_is_property:
                        protected_attributes.append(match.group(1).split("(")[0])
                        next_method_is_property = False
                    else:
                        protected_methods.append(match.group(1).split("(")[0])

        class_info = ClassInfo(
            package_name=package_name,
            module_name=module_name,
            class_name=class_name,
            super_class_name=super_class_name,
            used_classes=used_classes,
            public_attributes=public_attributes,
            protected_attributes=protected_attributes,
            public_methods=public_methods,
            protected_methods=protected_methods
        )
        return class_info
