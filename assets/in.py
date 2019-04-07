#!/usr/bin/env python3

import json
import os
import signal
import sys

import requests


def handler(signum, frame):
    print('Operation Timed Out', file=sys.stderr)
    exit(signum)


def call_spinnaker(source):
    return requests.get(
        source['base_url'] + 'applications/' + source['app_name'] + '/executions/search',
        params={'statuses': 'RUNNING', 'expand': 'true'}
    ).json()


def notify_spinnaker(source, output):
    return requests.get(
        source['base_url'] + 'concourse/stage/execution',
        params={'stageId': output['stage_guid'], 'job': output['job_name'], 'buildNumber': output['build_name']}
    ).ok


def capture_input():
    with sys.stdin as standard_in:
        request = json.load(standard_in)

    return request


def write_configuration(directory, source, configuration):
    with open(os.path.join(directory, source['path']), 'w') as config_file:
        for key, value in configuration:
            config_file.write(key + '=' + value + '\n')


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

                output = {}

                for application in payload:
                    if 'application' in application and application['application'] == source['app_name']:
                        if 'stages' in application:
                            for stage in application['stages']:
                                if 'id' in stage and stage['id'] == version \
                                        and 'type' in stage and stage['type'] == 'concourse' \
                                        and 'context' in stage:
                                    context = stage['context']
                                    if 'master' in context and master == context['master'] \
                                            and 'pipelineName' in context and pipeline_name == context['pipelineName'] \
                                            and 'resourceName' in context and resource_name == context['resourceName'] \
                                            and 'teamName' in context and team_name == context['teamName']:
                                        configuration = context['parameters']
                                        write_configuration(directory, source, configuration)
                                        output['version'] = {'stage_guid': version}
                                        output['metadata'] = []
                                        for key, value in configuration:
                                            output['metadata'].append({'name': key, 'value': value})

                                        if not notify_spinnaker(source, output):
                                            print('Failed to notify spinnaker', file=sys.stderr)
                                            exit(1)

            except KeyError as kerr:
                print('Unable to complete operation: ' + str(kerr) + '\n', file=sys.stderr)
                exit(1)
            else:
                print(json.dumps(output))

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
