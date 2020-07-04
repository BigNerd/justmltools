import sys
from unittest import TestCase
from typing import List, Tuple

from justmltools.cli.cli_arguments_parser import arg, CliArgumentsParser


class MyTestArguments:

    def __init__(self):
        self.__my_arg_1 = None
        self.__my_arg_2 = None
        self.__my_arg_3 = "my_arg_3_default_value"
        self.__my_arg_4 = []

    @arg(
        help="arg_1 required string",
        required=True
    )
    def my_arg_1(self) -> str:
        return self.__my_arg_1

    @arg(
        help="arg_2 required integer",
        required=True
    )
    def my_arg_2(self) -> int:
        return self.__my_arg_2

    @arg(
        help="arg_3 optional string"
    )
    def my_arg_3(self) -> str:
        return self.__my_arg_3

    @arg(
        help="arg_4 zero or more pairs of strings",
        action="append",
        nargs=2,
        metavar=("from", "to")
    )
    def my_arg_4(self) -> List[List[str]]:
        return self.__my_arg_4


class TestCliArgumentsParser(TestCase):

    def test_parse_with_required_arguments(self):
        sys.argv = ["python", "--my-arg-1", "my-arg-1-value", "--my-arg-2", "2"]
        arguments: MyTestArguments = CliArgumentsParser().parse(MyTestArguments())
        self.assertEqual("my-arg-1-value", arguments.my_arg_1())
        self.assertEqual(2, arguments.my_arg_2())
        self.assertEqual("my_arg_3_default_value", arguments.my_arg_3())

    def test_parse_with_required_but_wrongly_typed_arguments(self):
        sys.argv = ["python", "--my-arg-1", "my-arg-1-value", "--my-arg-2", "two"]
        with self.assertRaises(SystemExit):
            _: MyTestArguments = CliArgumentsParser().parse(MyTestArguments())

    def test_parse_without_required_arguments(self):
        sys.argv = ["python", "--my-arg-3", "my-arg-3-value"]
        with self.assertRaises(SystemExit):
            _: MyTestArguments = CliArgumentsParser().parse(MyTestArguments())

    def test_parse_with_optional_list_of_pairs_of_strings(self):
        sys.argv = ["python", "--my-arg-1", "my-arg-1-value", "--my-arg-2", "2", "--my-arg-4", "my-from-1", "my-to-1",
                    "--my-arg-4", "my-from-2", "my-to-2"]
        arguments: MyTestArguments = CliArgumentsParser().parse(MyTestArguments())
        self.assertEqual([["my-from-1", "my-to-1"], ["my-from-2", "my-to-2"]], arguments.my_arg_4())