#!/usr/bin/env python3

import json
import os
import signal
import sys

import requests

from assets import common


def notify_spinnaker(source, output):
    if 'user_name' in source and 'password' in source:
        return requests.post(
            source['base_url'] + 'concourse/stage/start',
            params={'stageId': output['version']['stage_guid'],
                    'job': output['job_name'],
                    'buildNumber': output['build_name']},
            auth=(source['user_name'], source['password'])
        ).ok
    else:
        return requests.post(
            source['base_url'] + 'concourse/stage/start',
            params={'stageId': output['version']['stage_guid'],
                    'job': output['job_name'],
                    'buildNumber': output['build_name']}
        ).ok


def write_configuration(directory, source, configuration):
    with open(os.path.join(directory, source['path']), 'w') as config_file:
        for key, value in configuration.items():
            config_file.write(key + '=' + value + '\n')


def process_in(directory=None):
    signal.alarm(20)

    try:
        try:
            request = common.capture_input()
        except json.decoder.JSONDecodeError:
            print('No configuration provided', file=sys.stderr)
            exit(1)
        else:
            try:
                version = common.extract_version(request)
                source = request['source']

                master = source['master']
                pipeline_name = source['pipeline_name']
                resource_name = source['resource_name']
                team_name = source['team_name']

                payload = common.call_spinnaker(source)

                output = {}

                for application in payload:
                    if 'application' in application and application['application'] == source['app_name']:
                        if 'stages' in application:
                            for stage in application['stages']:
                                if 'id' in stage and stage['id'] == version \
                                        and 'type' in stage and stage['type'] == 'concourse' \
                                        and 'context' in stage and 'tasks' in stage:
                                    context = stage['context']
                                    if 'master' in context and master == context['master'] \
                                            and 'pipelineName' in context and pipeline_name == context['pipelineName'] \
                                            and 'resourceName' in context and resource_name == context['resourceName'] \
                                            and 'teamName' in context and team_name == context['teamName']:
                                        for task in stage['tasks']:
                                            if 'status' in task and task['status'] == 'RUNNING' \
                                                    and 'name' in task \
                                                    and task['name'] == 'waitForConcourseJobStartTask':
                                                if 'parameters' in context:
                                                    configuration = context['parameters']
                                                else:
                                                    configuration = {}

                                                write_configuration(directory, source, configuration)
                                                output['version'] = {'stage_guid': version}
                                                output['job_name'] = os.environ.get('BUILD_JOB_NAME', 'job-unknown')
                                                output['build_name'] = os.environ.get('BUILD_NAME', 'build-number-name')
                                                output['metadata'] = []
                                                for key, value in configuration.items():
                                                    output['metadata'].append({'name': key, 'value': value})

                                                if not notify_spinnaker(source, output):
                                                    print('Failed to notify spinnaker', file=sys.stderr)
                                                    exit(1)

            except KeyError as kerr:
                print('Unable to complete operation: ' + str(kerr), file=sys.stderr)
                exit(1)
            else:
                if len(output) == 0:
                    print('No running Wait for Concourse task found', file=sys.stderr)
                    exit(1)

                print(json.dumps(output))

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(1)


def main(*args):
    directory = None
    if len(args) is 0:
        if len(sys.argv) < 2:
            print('Usage: %s PATH' % sys.argv[0], file=sys.stderr)
            exit(1)
        else:
            directory = sys.argv[1]
    else:
        directory = args[0]

    signal.signal(signal.SIGALRM, common.handler)

    process_in(directory)


if __name__ == '__main__':
    exit(main())
