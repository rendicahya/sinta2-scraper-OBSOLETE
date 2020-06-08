import json
from dicttoxml import dicttoxml
from dict2xml import dict2xml


def format_output(obj, output_format, pretty_print, xml_library):
    if output_format == 'json':
        json_indent = 4 if pretty_print else None
        output = json.dumps(obj, indent=json_indent)
    elif output_format == 'xml':
        if pretty_print:
            output = dict2xml(obj, wrap='author', indent='    ')
        elif xml_library == 'dict2xml':
            output = dict2xml(obj)
        elif xml_library == 'dicttoxml':
            output = dicttoxml(obj)
        else:
            output = dict2xml(obj)
    else:
        output = obj

    return output
