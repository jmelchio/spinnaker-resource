#!/usr/bin/env python3

import json
import os
import signal
import sys

import requests


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(1)


def call_spinnaker(source):
    return requests.get(
        source['base_url'] + 'api/path',
        params={'pipeline_id': source['pipeline_id'], 'resource_name': source['resource_name']}
    ).json()


def capture_input():
    with sys.stdin as standard_in:
        request = json.load(standard_in)

    return request


def process_in(directory=None):
    signal.alarm(5)

    try:
        try:
            request = capture_input()
        except json.decoder.JSONDecodeError:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            try:
                version = request['version']
                if len(version) == 0:
                    version = {"build_id": "0"}

                response = {"version": version, "metadata": []}
            except KeyError:
                response = {"version": {"build_id": "0"}, "metadata": []}

            print(json.dumps(response))

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(124)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print('Usage: %s PATH' % argv[0], file=sys.stderr)
        exit(1)

    signal.signal(signal.SIGALRM, handler)

    process_in(argv[1])


if __name__ == '__main__':
    exit(main())
