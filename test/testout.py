import json
import subprocess
import unittest


class TestOut(unittest.TestCase):

    def test_happy_path(self):
        with open('./data/in_request.json', 'r') as input_file:
            completed_process = subprocess.run(['/opt/resource/out', '/test/data'], stdin=input_file, capture_output=True)
            self.assertEqual(0, completed_process.returncode, 'process should return 0 exit')
            result = json.loads(completed_process.stdout)
            self.assertEqual('123456', result['version']['build_id'], 'version does not match expected value')
            self.assertEqual('somevalue', result['metadata'][0]['value'], 'return value does not match expected value')

    def test_should_time_out(self):
        try:
            completed_process = subprocess.run(['/opt/resource/out', '/test/data'], check=True, capture_output=True)
        except subprocess.CalledProcessError as cpe:
            self.assertEqual(124, cpe.returncode, 'process should have timed out')
        else:
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')

    def test_should_fail_to_parse(self):
        with open('./data/empty_file.json', 'r') as input_file:
            completed_process = subprocess.run(['/opt/resource/out', '/test/data'], stdin=input_file, capture_output=True)
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')
            error_message = completed_process.stderr.decode('utf-8')
            self.assertEqual('No configuration provided', error_message.split('\n', 1)[0], 'wrong error message')

    def test_should_fail_to_read_props(self):
        with open('./data/out_request_no_path.json', 'r') as input_file:
            completed_process = subprocess.run(['/opt/resource/out', '/test/data'], stdin=input_file, capture_output=True)
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')
            error_message = completed_process.stderr.decode('utf-8')
            self.assertEqual('No path provided', error_message.split('\n', 1)[0], 'wrong error message')

    def test_should_fail_to_read_props_v2(self):
        with open('./data/out_request_empty_path.json', 'r') as input_file:
            completed_process = subprocess.run(['/opt/resource/out', '/test/data'], stdin=input_file, capture_output=True)
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')
            error_message = completed_process.stderr.decode('utf-8')
            self.assertEqual('No path provided', error_message.split('\n', 1)[0], 'wrong error message')

    def test_should_fail_to_read_props_v3(self):
        with open('./data/out_request_empty_path.json', 'r') as input_file:
            completed_process = subprocess.run(['/opt/resource/out'], stdin=input_file, capture_output=True)
            self.assertNotEqual(0, completed_process.returncode, 'Non-zero return code expected')
            error_message = completed_process.stderr.decode('utf-8')
            self.assertEqual('Usage: /opt/resource/out PATH', error_message.split('\n', 1)[0], 'wrong error message')


if __name__ == '__main__':
    unittest.main()
