#!/usr/bin/env python3

import json
import requests
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(124)


def process_check():
    signal.alarm(5)

    try:
        try:
            with sys.stdin as standard_in:
                request = json.load(standard_in)
        except json.decoder.JSONDecodeError:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            try:
                version = request['version']['stage_guid']
                if version is None or len(version) == 0:
                    version = None

                source = request['source']

                response = requests.get(
                    source['base_url'] + 'api/path',
                    params={'pipeline_id': source['pipeline_id'], 'resource_name': source['resource_name']}
                )

                payload = json.loads(response.json())
                if payload is None or len(payload) == 0:
                    version = None
                else:
                    stage_guid = payload[0]['id']
                    if stage_guid is not None and stage_guid != version:
                        version = {'stage_guid': stage_guid}

                version_list = [version]
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
