from assets import check
from io import StringIO
import unittest
import json
import sys
from unittest.mock import patch

spinnaker_new_guid = '[{ "id": "testId", "parameters": { "testKey1": "testVal1", "testKey2": "testVal2" } }]'
spinnaker_empty_response = '[]'
spinnaker_no_id = '[{"parameters": { "testKey1": "testVal1", "testKey2": "testVal2" } }]'
spinnaker_multiple_values = '''
[{ "id": "testId0", "parameters": { "testKey1": "testVal0", "testKey2": "testVal1" } },
 { "id": "testId1", "parameters": { "testKey3": "testVal2", "testKey4": "testVal3" } },
 { "id": "testId2", "parameters": { "testKey1": "testVal4", "testKey2": "testVal5" } }]
'''
spinnaker_multiple_values_with_bad_value = '''
[{ "id": "testId0", "parameters": { "testKey1": "testVal0", "testKey2": "testVal1" } },
 { "badId": "testId1", "parameters": { "testKey3": "testVal2", "testKey4": "testVal3" } },
 { "id": "testId2", "parameters": { "testKey1": "testVal4", "testKey2": "testVal5" } }]
'''

concourse_check_with_version = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "pipeline_id": "123456", "resource_name": "resource name"}, 
"version": { "stage_guid": "1"}}
'''
                                          )
concourse_check_without_version = json.loads(''' { "source": 
{ "base_url": "http://spinnaker.gate:8084/", "pipeline_id": "123456", "resource_name": "resource name"}, 
"version": {}}
'''
                                             )

concourse_check_without_baseurl = json.loads(''' { "source": 
                                             { "pipeline_id": "123456", "resource_name": "resource name"}, 
                                             "version": {"stage_guid": "1"}}
                                             '''
                                             )


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
        self.assertEqual(out, '[{"stage_guid": "testId"}]\n', 'No new version returned')

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
            '[{"stage_guid": "testId0"}, {"stage_guid": "testId1"}, {"stage_guid": "testId2"}]\n',
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
        self.assertEqual(out, '[{"stage_guid": "testId"}]\n', 'No new version returned')

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
            '[{"stage_guid": "testId0"}, {"stage_guid": "testId2"}]\n',
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
