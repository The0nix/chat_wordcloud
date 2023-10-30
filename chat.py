import json
from pathlib import Path
from typing import Union


def flatten_message(message: Union[str, dict, list]) -> str:
    if isinstance(message, str):
        return message
    elif isinstance(message, dict):
        if message['type'] == 'link':
            return ''
        return flatten_message(message['text'])
    elif isinstance(message, list):
        return ' '.join(flatten_message(m) for m in message)
    else:
        raise ValueError(f'message should be str, list or dict. Got {type(message)}')


def read_messages(path: Union[Path, str, bytes]) -> list[str]:
    with open(path) as f:
        data = json.load(f)
    result = []
    for message in (m for m in data['messages'] if m['type'] == 'message'):
        text = flatten_message(message)
        if text:
            result.append(text)
    return result
