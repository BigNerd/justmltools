import argparse
from inspect import signature, Signature
from typing import Tuple, Union


def arg(
    help: str,
    required: bool = False,
    action: str = 'store',
    nargs: Union[int, str] = None,
    metavar: Union[str, Tuple] = None
):
    """
    This decorator stores meta data for command line argument parsing with an argument accessor method.
    The argument accessor method must have a signature of (self) -> return_type.
    Let the argument accessor method's name be x, then the command line argument name becomes --x.
    The argument accessor method's class must have a private attribute __x for storing the parsing result.

    See https://docs.python.org/3/library/argparse.html for a more detailed description of the following params:

    :param help: a help text describing the argument
    :param required: whether the argument is required or optional
    :param action: store, store_true, store_false, append, count
    :param nargs: the number of occurrences of this argument that can or must be supplied,
                  either an integer value > 1 or a string of the form '*' for zero or more or '+' for one or more
    :param metavar: gives name(s) to the expected argument value(s) in error and help outputs

    :return: the decorated function
    """
    def _arg(decorated_function):
        decorated_function.help = help
        decorated_function.required = required
        decorated_function.action = action
        decorated_function.nargs = nargs
        decorated_function.metavar = metavar
        return decorated_function
    return _arg


class CliArgumentsParser:

    def parse(self, arguments_object):
        argument_members = {}
        internal_parser = argparse.ArgumentParser()
        arguments_class_name = arguments_object.__class__.__name__
        for private_member in [name for name in dir(arguments_object) if name.startswith(f"_{arguments_class_name}__")]:
            derived_public_accessor_name = private_member.split('__')[1]
            try:
                cli_argument_name = '--' + derived_public_accessor_name.replace('_', '-')
                accessor_return_type = self.__get_method_return_type(arguments_object, derived_public_accessor_name)
                accessor_default_value = getattr(arguments_object, derived_public_accessor_name)()
                help = getattr(arguments_object, derived_public_accessor_name).help
                required = getattr(arguments_object, derived_public_accessor_name).required
                action = getattr(arguments_object, derived_public_accessor_name).action
                nargs = getattr(arguments_object, derived_public_accessor_name).nargs
                metavar = getattr(arguments_object, derived_public_accessor_name).metavar

                internal_parser.add_argument(
                    cli_argument_name,
                    type=accessor_return_type,
                    default=accessor_default_value,
                    help=help,
                    required=required,
                    action=action,
                    nargs=nargs,
                    metavar=metavar
                )
                argument_members[private_member] = derived_public_accessor_name
            except AttributeError as error:
                print(f"WARNING: Ignoring {private_member} in argument parsing, error is: {error}")
                continue  # skip this member, it does not qualify

        parsed_arguments, _ = internal_parser.parse_known_args()
        for argument_member in argument_members:
            argument_value = getattr(parsed_arguments, argument_members[argument_member])
            setattr(arguments_object, argument_member, argument_value)

        return arguments_object

    @staticmethod
    def __get_method_return_type(object, method):
        try:
            method_signature: Signature = signature(getattr(object, method))
            return_type = method_signature.return_annotation
            if not (return_type == str
                    or return_type == int
                    or return_type == float
                    or return_type == bool):
                # type is not supported easily by argparse, see https://docs.python.org/3/library/argparse.html#type
                return_type = None
        except AttributeError:
            raise AttributeError(f"{object} has no method {method}")
        return return_type

