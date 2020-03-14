from typing import List, Optional


class ClassInfo:

    def __init__(self,
                 package_name: str,
                 module_name: str,
                 class_name: Optional[str],
                 super_class_name: Optional[str],
                 used_classes: List[str],
                 public_attributes: List[str],
                 protected_attributes: List[str],
                 public_methods: List[str],
                 protected_methods: List[str]):
        self.__package_name: str = package_name
        self.__module_name: str = module_name
        self.__class_name: str = class_name
        self.__super_class_name: str = super_class_name
        self.__used_classes: List[str] = used_classes
        self.__public_attributes: List[str] = public_attributes
        self.__protected_attributes: List[str] = protected_attributes
        self.__public_methods: List[str] = public_methods
        self.__protected_methods: List[str] = protected_methods

    @property
    def package_name(self) -> str:
        return self.__package_name

    @property
    def module_name(self) -> str:
        return self.__module_name

    @property
    def class_name(self) -> Optional[str]:
        return self.__class_name

    @property
    def super_class_name(self) -> Optional[str]:
        return self.__super_class_name

    @property
    def used_classes(self) -> List[str]:
        return self.__used_classes

    @property
    def public_attributes(self) -> List[str]:
        return self.__public_attributes

    @property
    def protected_attributes(self) -> List[str]:
        return self.__protected_attributes

    @property
    def public_methods(self) -> List[str]:
        return self.__public_methods

    @property
    def protected_methods(self) -> List[str]:
        return self.__protected_methods

    @property
    def is_abstract(self) -> bool:
        is_abstract: bool = \
            self.super_class_name is not None and self.super_class_name == "abc.ABC"
        return is_abstract
