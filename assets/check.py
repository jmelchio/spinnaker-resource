#!/usr/bin/env python3

import json
import requests
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(124)


def call_spinnaker(source):
    return requests.get(
        source['base_url'] + 'api/path',
        params={'pipeline_id': source['pipeline_id'], 'resource_name': source['resource_name']}
    ).json()


def capture_input():
    with sys.stdin as standard_in:
        request = json.load(standard_in)

    return request


def process_check():
    signal.alarm(5)

    try:
        try:
            request = capture_input()
        except json.decoder.JSONDecodeError:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            try:
                if 'version' in request and 'stage_guid' in request['version']:
                    version = request['version']['stage_guid']
                else:
                    version = None

                source = request['source']

                payload = json.loads(call_spinnaker(source))

                version_list = []

                for item in payload:
                    if 'id' in item and item['id'] != version:
                        version_list.append({'stage_guid': item['id']})

            except KeyError:
                version_list = []

            print(json.dumps(version_list))

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(124)


def main():
    signal.signal(signal.SIGALRM, handler)

    process_check()


if __name__ == '__main__':
    exit(main())
