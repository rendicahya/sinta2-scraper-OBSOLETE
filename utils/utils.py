import json
from dicttoxml import dicttoxml
from dict2xml import dict2xml


def format_output(obj, output_format, pretty_print=None, xml_library='dicttoxml'):
    if output_format == 'json':
        json_indent = 4 if pretty_print else None
        output = json.dumps(obj, indent=json_indent)
    elif output_format == 'xml':
        output = dicttoxml(obj) if xml_library == 'dicttoxml' else dict2xml(obj)
    else:
        output = obj

    return output
