import json
import subprocess
import unittest


class TestCheck(unittest.TestCase):

    def test_happy_path_no_new(self):
        with open('./data/check_request.json', 'r') as input_file:
            completed_process = subprocess.run('/opt/resource/check', stdin=input_file, capture_output=True)
            self.assertEqual(0, completed_process.returncode, 'process should return 0 exit')
            result = json.loads(completed_process.stdout)
            self.assertEqual(result[0]['spinnaker_request'], '1', 'version does not match expected value')

    def test_happy_path_has_new(self):
        with open('./data/check_request.json', 'r') as input_file:
            completed_process = subprocess.run('/opt/resource/check', stdin=input_file, capture_output=True)
            self.assertEqual(0, completed_process.returncode, 'process should return 0 exit')
            result = json.loads(completed_process.stdout)
            self.assertEqual(result[0]['spinnaker_request'], '2', 'version does not match expected value')

    def test_should_time_out(self):
        try:
            completed_process = subprocess.run('/opt/resource/check', check=True, capture_output=True)
        except subprocess.CalledProcessError as cpe:
            self.assertEqual(124, cpe.returncode, 'process should have timed out')
        else:
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')

    def test_should_fail_to_parse(self):
        with open('./data/empty_file.json', 'r') as input_file:
            completed_process = subprocess.run('/opt/resource/check', stdin=input_file, capture_output=True)
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')
            error_message = completed_process.stderr.decode('utf-8')
            self.assertEqual('No configuration provided', error_message.split('\n', 1)[0], 'wrong error message')

    def test_should_return_first_version(self):
        with open('./data/check_request_no_version.json', 'r') as input_file:
            completed_process = subprocess.run('/opt/resource/check', stdin=input_file, capture_output=True)
            self.assertEqual(0, completed_process.returncode, 'process should return 0 exit')
            result = json.loads(completed_process.stdout)
            self.assertEqual(result[0]['build_id'], '0', 'version does not match expected value')

    def test_should_return_first_version_v2(self):
        with open('./data/check_request_empty_version.json', 'r') as input_file:
            completed_process = subprocess.run('/opt/resource/check', stdin=input_file, capture_output=True)
            self.assertEqual(0, completed_process.returncode, 'process should return 0 exit')
            result = json.loads(completed_process.stdout)
            self.assertEqual(result[0]['build_id'], '0', 'version does not match expected value')


if __name__ == '__main__':
    unittest.main()
