from flask import Response

import json
from . import xml_builder

from typing import Dict, Callable, Any, Set


formats_and_converters: Dict[str, Callable[[Any], str]]
formats_and_mimes: Dict[str, str]
supported_formats: Set[str]


def convert_to_format(struct, format: str) -> Response:
    if format not in supported_formats:
        raise ValueError(f'Format {format} is not supported')

    converter = formats_and_converters[format]
    mime = formats_and_mimes[format]

    converted = converter(struct)

    return Response(converted, mimetype=mime)    


def to_json(struct) -> str:
    return json.dumps(struct)


def to_xml(struct) -> str:
    converted: str
    converted = xml_builder.dumps(struct)

    return converted


formats_and_converters = {
    'json': to_json,
    'xml': to_xml,
}

formats_and_mimes = {
    'json': 'text/json',
    'xml': 'text/xml',
}

supported_formats = formats_and_converters.keys() & formats_and_mimes.keys()
