import json

from dict2xml import dict2xml
from string_utils.validation import is_integer, is_decimal


def format_output(obj, output_format):
    if output_format == 'json':
        output = json.dumps(obj)
    elif output_format == 'json-pretty':
        output = json.dumps(obj, indent=4)
    elif output_format == 'xml':
        output = dict2xml(obj, wrap='author')
    elif output_format == 'xml-pretty':
        output = dict2xml(obj, wrap='author', indent='    ')
    else:
        output = obj

    return output


def cast(string: str):
    if string is None:
        return None

    string = string.strip()

    if is_integer(string):
        return int(string)
    elif is_decimal(string):
        return float(string)
    elif string == '-':
        return None
    else:
        return string


def listify(param):
    return [param] if type(param) not in [list, tuple] else param
