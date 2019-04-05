from assets import check
from io import StringIO
import unittest
import json
import sys
from unittest.mock import patch

spinnaker_new_guid = '''
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
                        "name": "waitForJudgment",
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
'''
spinnaker_empty_response = '[]'
spinnaker_no_id = '''
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
                    "resourceName": "spin-resource"
                },
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
'''
spinnaker_multiple_values = '''
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
                        "name": "waitForJudgment",
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
'''
spinnaker_multiple_values_with_bad_value = '''
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
                    "resourceName": "spin-resource"
                },
                "badid": "01D7N3NNCG0GBKK28RS25R4HX4",
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
                "type": "concourse"
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
                        "name": "waitForJudgment",
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
'''

concourse_check_with_version = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "app_name": "metricsdemo", "master": "some-master", "team_name": "A-team",
"pipeline_name": "some-pipeline", "resource_name": "spin-resource"}, 
"version": { "stage_guid": "1"}} ''')

concourse_check_without_version = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "app_name": "metricsdemo", "master": "some-master", "team_name": "A-team",
"pipeline_name": "some-pipeline", "resource_name": "spin-resource"}, "version": {}} ''')

concourse_check_without_baseurl = json.loads('''{ "source": { "app_name": "metricsdemo", "master": "some-master"
, "team_name": "A-team", "pipeline_name": "some-pipeline", "resource_name": "spin-resource"}, 
"version": {"stage_guid": "1"}}''')


class TestCheck(unittest.TestCase):

    @patch('assets.check.call_spinnaker', return_value=spinnaker_new_guid)
    @patch('assets.check.capture_input', return_value=concourse_check_with_version)
    def test_unit_happy_path_new_version(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out, '[{"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}]\n', 'No new version returned')

    @patch('assets.check.call_spinnaker', return_value=spinnaker_multiple_values)
    @patch('assets.check.capture_input', return_value=concourse_check_with_version)
    def test_unit_happy_path_new_versions(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(
            out,
            '[{"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}, {"stage_guid": "01D7N3NNCGZ2PWFS2FKYBS2FFV"}]\n',
            'No new version returned'
        )

    @patch('assets.check.call_spinnaker', return_value=spinnaker_new_guid)
    @patch('assets.check.capture_input', return_value=concourse_check_without_version)
    def test_unit_happy_path_no_existing_version(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out, '[{"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}]\n', 'No new version returned')

    @patch('assets.check.call_spinnaker', return_value=spinnaker_empty_response)
    @patch('assets.check.capture_input', return_value=concourse_check_without_version)
    def test_unit_happy_path_no_new_version(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out, '[]\n', 'No empty list returned')

    @patch('assets.check.call_spinnaker', return_value=spinnaker_no_id)
    @patch('assets.check.capture_input', return_value=concourse_check_without_version)
    def test_unit_crappy_path_missing_id(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out, '[]\n', 'No empty list returned')

    @patch('assets.check.call_spinnaker', return_value=spinnaker_multiple_values_with_bad_value)
    @patch('assets.check.capture_input', return_value=concourse_check_with_version)
    def test_unit_crappy_path_new_versions_bad_id(self, call_spinnaker, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(
            out,
            '[{"stage_guid": "01D7N3NNCG0GBKK28RS25R4HX4"}, {"stage_guid": "01D7N3NNCGZ2PWFS2FKYBS2FFV"}]\n',
            'No new version returned'
        )

    @patch('assets.check.capture_input', return_value=concourse_check_without_baseurl)
    def test_unit_crappy_path_missing_base_url(self, capture_input):
        backup = sys.stdout
        sys.stdout = StringIO()
        check.main()
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = backup
        self.assertEqual(out, '[]\n', 'No empty list returned')


if __name__ == '__main__':
    unittest.main()
