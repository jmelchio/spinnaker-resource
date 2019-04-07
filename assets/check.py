#!/usr/bin/env python3

import json
import requests
import signal
import sys


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(signum)


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
                master = source['master']
                pipeline_name = source['pipeline_name']
                resource_name = source['resource_name']
                team_name = source['team_name']

                payload = json.loads(call_spinnaker(source))

                version_list = []

                for application in payload:
                    if 'application' in application and application['application'] == source['app_name']:
                        if 'stages' in application:
                            for stage in application['stages']:
                                if 'id' in stage and stage['id'] != version \
                                        and 'type' in stage and stage['type'] == 'concourse' \
                                        and 'context' in stage:
                                    context = stage['context']
                                    if 'master' in context and master == context['master'] \
                                            and 'pipelineName' in context and pipeline_name == context['pipelineName'] \
                                            and 'resourceName' in context and resource_name == context['resourceName'] \
                                            and 'teamName' in context and team_name == context['teamName']:
                                        version_list.append({'stage_guid': stage['id']})

            except KeyError:
                version_list = []

            print(json.dumps(version_list))

    except SystemExit as sysex:
        print('System Exit detected: ' + str(sysex.code), file=sys.stderr)
        exit(1)


def main():
    signal.signal(signal.SIGALRM, handler)

    process_check()


if __name__ == '__main__':
    exit(main())
