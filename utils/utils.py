import json

import pandas as pd
from dict2xml import dict2xml
from string_utils.validation import is_integer, is_decimal


def format_output(obj, output_format):
    if output_format == 'json':
        return json.dumps(obj)
    elif output_format == 'json-pretty':
        return json.dumps(obj, indent=4)
    elif output_format == 'xml':
        return dict2xml(obj, wrap='author')
    elif output_format == 'xml-pretty':
        return dict2xml(obj, wrap='author', indent='    ')
    elif output_format == 'dataframe':
        return pd.DataFrame.from_dict(obj)
    else:
        return obj


def cast(string: str):
    if not string:
        return None

    string = string.strip()

    if is_integer(string):
        return int(string)
    elif is_decimal(string):
        return float(string)
    elif string == '-' or string == '':
        return None
    else:
        return string


def listify(param) -> list:
    return [param] if type(param) not in [list, tuple] else param
