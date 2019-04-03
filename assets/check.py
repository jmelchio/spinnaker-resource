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
                version = request['version']
                if version is None or len(version) == 0:
                    version = None

                source = request['source']
                baseUrl = source['baseUrl']
                pipelineId = source['pipeline_id']
                resourceName = source['resource_name']

                # create REST call using source.baseUrl and request using stageId
                response = requests.get(
                    baseUrl + 'api/path',
                    params={'pipeline_id': pipelineId, 'resource_name': resourceName}
                )

                payload = json.loads(response.json())
                if payload is None or len(payload) == 0:
                    version = None
                else:
                    stage_guid = payload[0]['id']
                    # if stage_guid


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
