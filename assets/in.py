#!/usr/bin/env python3

import json
import os
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(1)


def process_in():
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


def main():
    signal.signal(signal.SIGALRM, handler)

    process_in()


if __name__ == '__main__':
    exit(main())
