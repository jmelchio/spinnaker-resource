#!/usr/bin/env python3

import json
import sys

import requests


def handler(signum, _frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(signum)


def capture_input():
    with sys.stdin as standard_in:
        return json.load(standard_in)

def call_spinnaker(source):
    if 'user_name' in source and 'password' in source:
        return requests.get(
            source['base_url'] + 'applications/' + source['app_name'] + '/executions/search',
            params={'statuses': 'RUNNING', 'expand': 'true'},
            auth=(source['user_name'], source['password'])
        ).json()
    else:
        return requests.get(
            source['base_url'] + 'applications/' + source['app_name'] + '/executions/search',
            params={'statuses': 'RUNNING', 'expand': 'true'}
        ).json()


def extract_version(request):
    if 'version' in request and request['version'] is not None and 'stage_guid' in request['version']:
        version = request['version']['stage_guid']
    else:
        version = None

    return version
