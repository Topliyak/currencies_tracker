from flask import Response

from json import dumps
from dicttoxml import dicttoxml

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
    return dumps(struct)


def to_xml(struct) -> str:
    converted: str
    
    converted = dicttoxml(
        struct, 
        attr_type=False, 
        return_bytes=False
    )

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
