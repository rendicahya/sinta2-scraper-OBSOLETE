import json
from dicttoxml import dicttoxml


def format_output(obj, output_format, pretty_print=None):
    if output_format == 'json':
        json_indent = 4 if pretty_print else None
        output = json.dumps(obj, indent=json_indent)
    elif output_format == 'xml':
        output = dicttoxml(obj)
    else:
        output = obj

    return output
