import json


def parse_output(response_text):
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as e:
        parsed = {}
    return parsed
