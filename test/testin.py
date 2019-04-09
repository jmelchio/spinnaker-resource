import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from assets import inscript

spinnaker_waitforconcourse_running = json.loads('''
[
    {
        "application": "metricsdemo",
        "authentication": {
            "allowedAccounts": [
                "seoul",
                "montclair",
                "atherton"
            ],
            "user": "anonymous"
        },
        "buildTime": 1554412918160,
        "canceled": false,
        "id": "01D7N3NNCGRF14VNPHMM46X19X",
        "initialConfig": {},
        "keepWaitingPipelines": false,
        "limitConcurrent": true,
        "name": "block",
        "notifications": [],
        "origin": "api",
        "pipelineConfigId": "4652d7ac-e9af-41b2-b41f-a946e24354f2",
        "stages": [
            {
                "context": {
                    "master": "some-master",
                    "teamName": "A-team",
                    "pipelineName": "some-pipeline",
                    "resourceName": "spin-resource",
                    "parameters": {
                        "thing_one": "one",
                        "thing_two": "two"
                    }
                },
                "id": "01D7N3NNCG0GBKK28RS25R4HX4",
                "name": "Manual Judgment",
                "outputs": {},
                "refId": "1",
                "requisiteStageRefIds": [],
                "startTime": 1554412918193,
                "status": "RUNNING",
                "tasks": [
                    {
                        "id": "1",
                        "implementingClass": "com.netflix.spinnaker.orca.echo.pipeline.ManualJudgmentStage$WaitForManualJudgmentTask",
                        "loopEnd": false,
                        "loopStart": false,
                        "name": "waitForConcourseJobStartTask",
                        "stageEnd": true,
                        "stageStart": true,
                        "startTime": 1554412918208,
                        "status": "RUNNING"
                    }
                ],
                "type": "concourse"
            }
        ],
        "startTime": 1554412918173,
        "status": "RUNNING",
        "systemNotifications": [],
        "trigger": {
            "artifacts": [],
            "dryRun": false,
            "enabled": false,
            "eventId": "fdc68837-d4ae-421a-817d-c9d31d532939",
            "notifications": [],
            "parameters": {},
            "rebake": false,
            "resolvedExpectedArtifacts": [],
            "strategy": false,
            "type": "manual",
            "user": "anonymous"
        },
        "type": "PIPELINE"
    }
]
''')

spinnaker_waitforconcourse_completed = json.loads('''
[
    {
        "application": "metricsdemo",
        "authentication": {
            "allowedAccounts": [
                "seoul",
                "montclair",
                "atherton"
            ],
            "user": "anonymous"
        },
        "buildTime": 1554412918160,
        "canceled": false,
        "id": "01D7N3NNCGRF14VNPHMM46X19X",
        "initialConfig": {},
        "keepWaitingPipelines": false,
        "limitConcurrent": true,
        "name": "block",
        "notifications": [],
        "origin": "api",
        "pipelineConfigId": "4652d7ac-e9af-41b2-b41f-a946e24354f2",
        "stages": [
            {
                "context": {
                    "master": "some-master",
                    "teamName": "A-team",
                    "pipelineName": "some-pipeline",
                    "resourceName": "spin-resource",
                    "parameters": {
                        "thing_one": "one",
                        "thing_two": "two"
                    }
                },
                "id": "01D7N3NNCG0GBKK28RS25R4HX4",
                "name": "Manual Judgment",
                "outputs": {},
                "refId": "1",
                "requisiteStageRefIds": [],
                "startTime": 1554412918193,
                "status": "RUNNING",
                "tasks": [
                    {
                        "id": "1",
                        "implementingClass": "com.netflix.spinnaker.orca.echo.pipeline.ManualJudgmentStage$WaitForManualJudgmentTask",
                        "loopEnd": false,
                        "loopStart": false,
                        "name": "waitForConcourseJobStartTask",
                        "stageEnd": true,
                        "stageStart": true,
                        "startTime": 1554412918208,
                        "status": "COMPLETED"
                    }
                ],
                "type": "concourse"
            }
        ],
        "startTime": 1554412918173,
        "status": "RUNNING",
        "systemNotifications": [],
        "trigger": {
            "artifacts": [],
            "dryRun": false,
            "enabled": false,
            "eventId": "fdc68837-d4ae-421a-817d-c9d31d532939",
            "notifications": [],
            "parameters": {},
            "rebake": false,
            "resolvedExpectedArtifacts": [],
            "strategy": false,
            "type": "manual",
            "user": "anonymous"
        },
        "type": "PIPELINE"
    }
]
''')

spinnaker_multiple_values = json.loads('''
[
    {
        "application": "metricsdemo",
        "authentication": {
            "allowedAccounts": [
                "seoul",
                "montclair",
                "atherton"
            ],
            "user": "anonymous"
        },
        "buildTime": 1554412918160,
        "canceled": false,
        "id": "01D7N3NNCGRF14VNPHMM46X19X",
        "initialConfig": {},
        "keepWaitingPipelines": false,
        "limitConcurrent": true,
        "name": "block",
        "notifications": [],
        "origin": "api",
        "pipelineConfigId": "4652d7ac-e9af-41b2-b41f-a946e24354f2",
        "stages": [
            {
                "context": {
                    "failPipeline": true,
                    "instructions": "Should I complete?",
                    "judgmentInputs": [],
                    "notifications": []
                },
                "id": "01D7N3NNCG0GBKK28RS25R4HX4",
                "name": "Manual Judgment",
                "outputs": {},
                "refId": "1",
                "requisiteStageRefIds": [],
                "startTime": 1554412918193,
                "status": "RUNNING",
                "tasks": [
                    {
                        "id": "1",
                        "implementingClass": "com.netflix.spinnaker.orca.echo.pipeline.ManualJudgmentStage$WaitForManualJudgmentTask",
                        "loopEnd": false,
                        "loopStart": false,
                        "name": "waitForJudgment",
                        "stageEnd": true,
                        "stageStart": true,
                        "startTime": 1554412918208,
                        "status": "RUNNING"
                    }
                ],
                "type": "manualJudgment"
            },
            {
                "context": {
                    "master": "some-master",
                    "teamName": "A-team",
                    "pipelineName": "some-pipeline",
                    "resourceName": "spin-resource"
                },
                "id": "01D7N3NNCG0GBKK28RS25R4HX4",
                "name": "Manual Judgment",
                "outputs": {},
                "refId": "1",
                "requisiteStageRefIds": [],
                "startTime": 1554412918193,
                "status": "RUNNING",
                "tasks": [
                    {
                        "id": "1",
                        "implementingClass": "com.netflix.spinnaker.orca.echo.pipeline.ManualJudgmentStage$WaitForManualJudgmentTask",
                        "loopEnd": false,
                        "loopStart": false,
                        "name": "waitForConcourseJobStartTask",
                        "stageEnd": true,
                        "stageStart": true,
                        "startTime": 1554412918208,
                        "status": "RUNNING"
                    }
                ],
                "type": "concourse"
            },
            {
                "context": {
                    "master": "some-master",
                    "teamName": "A-team",
                    "pipelineName": "some-pipeline",
                    "resourceName": "spin-resource"
                },
                "id": "01D7N3NNCGZ2PWFS2FKYBS2FFV",
                "name": "Clone Server Group",
                "outputs": {},
                "refId": "2",
                "requisiteStageRefIds": [
                    "1"
                ],
                "status": "NOT_STARTED",
                "tasks": [],
                "type": "concourse"
            }
        ],
        "startTime": 1554412918173,
        "status": "RUNNING",
        "systemNotifications": [],
        "trigger": {
            "artifacts": [],
            "dryRun": false,
            "enabled": false,
            "eventId": "fdc68837-d4ae-421a-817d-c9d31d532939",
            "notifications": [],
            "parameters": {},
            "rebake": false,
            "resolvedExpectedArtifacts": [],
            "strategy": false,
            "type": "manual",
            "user": "anonymous"
        },
        "type": "PIPELINE"
    }
]
''')

concourse_in_match_version = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "app_name": "metricsdemo", "master": "some-master", "team_name": "A-team",
"pipeline_name": "some-pipeline", "resource_name": "spin-resource", "path": "file.props"}, 
"version": { "stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}} ''')

concourse_in_match_version_two = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "app_name": "metricsdemo", "master": "some-master", "team_name": "A-team",
"pipeline_name": "some-pipeline", "resource_name": "spin-resource", "path": "file_two.props"}, 
"version": { "stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}} ''')

concourse_in_match_version_three = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "app_name": "metricsdemo", "master": "some-master", "team_name": "A-team",
"pipeline_name": "some-pipeline", "resource_name": "spin-resource", "path": "file_three.props"}, 
"version": { "stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}} ''')

concourse_in_without_baseurl = json.loads('''{ "source": { "app_name": "metricsdemo", "master": "some-master"
, "team_name": "A-team", "pipeline_name": "some-pipeline", "resource_name": "spin-resource"}, 
"version": {"stage_guid": "1"}}''')


class TestIn(unittest.TestCase):

    @patch('assets.inscript.call_spinnaker', return_value=spinnaker_waitforconcourse_running)
    @patch('assets.inscript.capture_input', return_value=concourse_in_match_version)
    @patch('assets.inscript.notify_spinnaker', return_value=True)
    def test_unit_happy_path(self, call_spinnaker, capture_input, notify_spinnaker):
        backup = sys.stdout
        sys.stdout = StringIO()
        inscript.main('/tmp/')
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out,
                         '{"version": {"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}, "job_name": "job-unknown", \
"build_name": "build-number-name", "metadata": [{"name": "thing_one", "value": "one"}, \
{"name": "thing_two", "value": "two"}]}\n',
                         'Wrong information returned from in script')
        self.assertTrue(os.path.isfile('/tmp/file.props'), 'File does not exist.')
        with open('/tmp/file.props', 'r') as config_file:
            contents = config_file.read()
            self.assertEqual(contents, 'thing_one=one\nthing_two=two\n', 'String not found')
        os.remove('/tmp/file.props')

    @patch('assets.inscript.call_spinnaker', return_value=spinnaker_multiple_values)
    @patch('assets.inscript.capture_input', return_value=concourse_in_match_version_two)
    @patch('assets.inscript.notify_spinnaker', return_value=True)
    def test_unit_happy_path_no_parameters(self, call_spinnaker, capture_input, notify_spinnaker):
        backup = sys.stdout
        sys.stdout = StringIO()
        inscript.main('/tmp/')
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out,
                         '{"version": {"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}, "job_name": "job-unknown", \
"build_name": "build-number-name", "metadata": []}\n', 'Wrong information returned from in script')
        self.assertTrue(os.path.isfile('/tmp/file_two.props'), 'File does not exist.')
        with open('/tmp/file_two.props', 'r') as config_file:
            contents = config_file.read()
            self.assertEqual(contents, '', 'File not empty')
        os.remove('/tmp/file_two.props')

    @patch('assets.inscript.call_spinnaker', return_value=spinnaker_waitforconcourse_completed)
    @patch('assets.inscript.capture_input', return_value=concourse_in_match_version_three)
    @patch('assets.inscript.notify_spinnaker', return_value=True)
    def test_unit_crappy_path_no_running_wait_task(self, call_spinnaker, capture_input, notify_spinnaker):
        backup = sys.stderr
        sys.stderr = StringIO()

        with self.assertRaises(SystemExit) as context:
            inscript.main('/tmp/')

        err = sys.stderr.getvalue()
        sys.stderr.close()
        sys.stderr = backup
        self.assertEqual(str(context.exception), '1', 'Return code of `1` expected')
        self.assertEqual(err, 'No running Wait for Concourse task found\nSystem Exit detected\n')

    @patch('assets.inscript.capture_input', return_value=concourse_in_without_baseurl)
    def test_unit_crappy_path_missing_base_url(self, capture_input):
        backup = sys.stderr
        sys.stderr = StringIO()

        with self.assertRaises(SystemExit) as context:
            inscript.main('/tmp/')

        err = sys.stderr.getvalue()
        sys.stderr.close()
        sys.stderr = backup
        self.assertEqual(str(context.exception), '1', 'Return code of `1` expected')
        self.assertEqual(err, 'Unable to complete operation: \'base_url\'\nSystem Exit detected\n',
                         'Expected error message about base_url')


class TestTimeOut(unittest.TestCase):

    def test_unit_crappy_path_timeout(self):
        backup = sys.stderr
        sys.stderr = StringIO()

        with self.assertRaises(SystemExit) as context:
            inscript.main('/tmp/')

        err = sys.stderr.getvalue()
        sys.stderr.close()
        sys.stderr = backup
        self.assertEqual(str(context.exception), '1', 'Return code of `1` expected')


if __name__ == '__main__':
    unittest.main()
