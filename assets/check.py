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
        source['base_url'] + 'applications/' + source['app_name'] + '/executions/search',
        params={'statuses': 'RUNNING', 'expand': 'true'}
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

                for application in payload:
                    if 'application' in application and application['application'] == source['app_name']:
                        if 'stages' in application:
                            for stage in application['stages']:
                                if 'id' in stage and stage['id'] != version \
                                        and 'type' in stage and stage['type'] == 'concourse':
                                    version_list.append({'stage_guid': stage['id']})

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
