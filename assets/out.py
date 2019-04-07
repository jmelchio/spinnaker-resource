#!/usr/bin/env python3

import json
import os
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(signum)


def process_out(directory=None):
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
                path = request['source']['path']
                if len(path) == 0:
                    raise KeyError

            except KeyError:
                print('No path provided', file=sys.stderr)
                exit(1)
            else:
                metadata = []
                with open(os.path.join(directory, path), 'r') as props_file:
                    for line in props_file.readlines():
                        parts = line.split('=')
                        if len(parts) == 2:
                            metadata.append({"name": parts[0].strip(), "value": parts[1].strip()})

                response = {
                    "version": {
                        "build_id": os.getenv('BUILD_ID', '123456')
                    },
                    "metadata": metadata
                }
                print(json.dumps(response))

    except SystemExit as sysex:
        print('System Exit detected', file=sys.stderr)
        exit(sysex.code)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print('Usage: %s PATH' % argv[0], file=sys.stderr)
        exit(1)

    signal.signal(signal.SIGALRM, handler)

    process_out(argv[1])


if __name__ == '__main__':
    exit(main())
