# Standard lib imports
import json
import os


def load_schema(filename):
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, '{}.json'.format(filename))

    with open(os.path.abspath(path), 'r') as f:
        data = f.read()

    return json.loads(data)
