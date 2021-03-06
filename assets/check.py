#!/usr/bin/env python3

import json
import signal
import sys

from assets import common


def process_check():
    signal.alarm(5)

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

                if 'master' in source:
                    master = source['master']
                else:
                    master = None
                pipeline_name = source['pipeline_name']
                resource_name = source['resource_name']
                team_name = source['team_name']

                payload = common.call_spinnaker(source)

                version_list = []

                for application in payload:
                    if 'application' in application and application['application'] == source['app_name']:
                        if 'stages' in application:
                            for stage in application['stages']:
                                if 'id' in stage and stage['id'] != version \
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
                                                version_list.append({'stage_guid': stage['id']})

            except KeyError:
                version_list = []

            print(json.dumps(version_list))

    except SystemExit:
        print('System Exit detected', file=sys.stderr)
        exit(1)


def main():
    signal.signal(signal.SIGALRM, common.handler)

    process_check()


if __name__ == '__main__':
    exit(main())
