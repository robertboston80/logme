import os
import ast
from typing import List, Union

from pathlib import Path
from contextlib import contextmanager

from .exceptions import InvalidOption, LogmeError


def conf_to_dict(conf_section: List[tuple]) -> dict:
    """
    Converting the config section to a dictionary format

    :param conf_section: values from config.items('section')
    """

    return {i[0]: conf_item_to_dict(i[1]) if '\n' in i[1] else i[1]
            for i in conf_section}


def conf_item_to_dict(parse_option: str) -> dict:
    """
    Map the configuration item(such as 'FileHandler' section) to dict.
    * Do not pass in the whole config section!*

    :param: parse_option: values from config.get('section', 'option')
    """
    try:
        str_split = parse_option.strip().split('\n')
        mapped_list = list(map(lambda x: x.split(': '), str_split))

        strip_blank_recursive(mapped_list)

        return dict(mapped_list)
    except AttributeError:
        raise InvalidOption(f"option passed must be a string value, not type of '{type(parse_option).__name__}'.")
    except ValueError:
        raise InvalidOption(f"{parse_option} is not a valid option, please follow the convention of 'key: value'")


def dict_to_conf(parse_dict: dict) -> dict:
    """
    flatten nested dict for logme configuration file
    """
    flattened = {}

    for k, v in parse_dict.items():

        if isinstance(v, str):
            str_val = v
        elif isinstance(v, dict):
            val_list = [f'{k1}: {v1}' for k1, v1 in v.items()]

            str_val = '\n' + '\n'.join(val_list)
        else:
            raise ValueError(f"all values in the dict must be dict or string value, "
                             f"'{type(v).__name__}' is not allowed!")

        flattened[k] = str_val

    return flattened


def strip_blank_recursive(nested_list: list):
    """
    Strip blank space or newline characters recursively for a nested list

    *This updates the original list passed in*

    """
    if not isinstance(nested_list, list):
        raise ValueError(f"iterable passed must be type of list. not '{type(nested_list).__name__}'")

    for i, v in enumerate(nested_list):
        if isinstance(v, list):
            strip_blank_recursive(v)
        elif isinstance(v, str):
            if v.strip() in ['True', 'False', 'None']:
                val_ = ast.literal_eval(v.strip())
            else:
                val_ = v.strip()

            nested_list[i] = val_


def ensure_dir(dir_path: Union[Path, str], path_type: str='parent'):
    """
    Ensure the existence of the directory,

    :param dir_path: the path to be ensured
    :param path_type: current - ensure the passed in directory exists, typically used when


    """
    path_mapping = {
        'current': Path(dir_path).resolve(),
        'parent': Path(dir_path).parent.resolve()
    }

    try:
        dir_abs = path_mapping[path_type]

        if not dir_abs.exists():
            dir_abs.mkdir(parents=True, exist_ok=True)
    except KeyError:
        raise InvalidOption(f"{path_type} is not a valid option, please pass in either 'parent' or 'current'")


def check_scope(scope: str, options: list) -> bool:
    """
    check if the scope passed is within the options.
    Used both in logme/__init__.py and providers.LogDecorator

    """
    if scope not in options:
        raise LogmeError(f"scope '{scope}' is not supported, "
                         f"please use one of {options}")

    return True


@contextmanager
def cd(dir_path: str):
    """
    Context manager for cd, change back to original directory when done
    """
    cwd = os.getcwd()
    try:
        os.chdir(os.path.expanduser(dir_path))
        yield
    finally:
        os.chdir(cwd)
